from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime
import urllib.parse
import json
import re
import io
import os
import traceback
import sys
import signal
import time

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
DENUNCIAS_FILE = ROOT / "denuncias.txt"
UPLOADS_DIR = ROOT / "uploads"

DENUNCIAS_FILE.touch(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)

# Variável global para controlar o servidor
servidor_global = None


def signal_handler(sig, frame):
    """Trata Ctrl+C para desligar o servidor gracefully"""
    print("\n\nEncerrando servidor...")
    if servidor_global:
        servidor_global.shutdown()
    sys.exit(0)


def salvar_denuncia(nome: str, contato: str, local: str, descricao: str, foto_path: str | None) -> None:
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    conteudo = (
        "\n" + "=" * 40 + "\n"
        f"DATA: {data_hora}\n"
        f"NOME: {nome or 'Não informado'}\n"
        f"CONTATO: {contato or 'Não informado'}\n"
        f"LOCAL: {local}\n"
        "DESCRIÇÃO:\n"
        f"{descricao}\n"
    )
    if foto_path:
        conteudo += f"FOTO: {foto_path}\n"
    conteudo += "=" * 40 + "\n"

    with open(DENUNCIAS_FILE, "a", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)


def enviar_resposta(handler, data: dict, status: int = 200) -> None:
    try:
        resposta = json.dumps(data, ensure_ascii=False).encode("utf-8")
        handler.send_response(status)
        handler.send_header("Content-Type", "application/json; charset=utf-8")
        handler.send_header("Content-Length", str(len(resposta)))
        handler.send_header("Access-Control-Allow-Origin", "*")
        handler.end_headers()
        handler.wfile.write(resposta)
    except Exception as e:
        print(f"Erro ao enviar resposta: {e}")
        try:
            handler.send_error(500, "Erro ao processar resposta")
        except:
            pass


def _parse_multipart(body: bytes, content_type: str) -> dict:
    """Parse a simple multipart/form-data body.
    Returns a mapping field -> value where value is str for regular fields
    or a dict {'filename': ..., 'content': bytes} for file fields.
    This is a minimal parser and not a full RFC implementation; it's
    sufficient for basic browser form uploads.
    """
    m = re.search(r'boundary=(?P<boundary>.*)', content_type)
    if not m:
        return {}
    boundary = m.group('boundary')
    if boundary.startswith('"') and boundary.endswith('"'):
        boundary = boundary[1:-1]
    boundary_bytes = ("--" + boundary).encode('utf-8')

    parts = body.split(boundary_bytes)
    fields = {}
    for part in parts:
        if not part or part == b'--' or part == b'--\r\n':
            continue
        part = part.lstrip(b'\r\n')
        if not part:
            continue
        try:
            header_raw, content = part.split(b"\r\n\r\n", 1)
        except ValueError:
            continue
        content = content.rstrip(b"\r\n")
        headers = header_raw.decode('utf-8', errors='replace').split('\r\n')
        disp = None
        filename = None
        name = None
        for h in headers:
            if h.lower().startswith('content-disposition:'):
                disp = h
                # exemplo: form-data; name="campo"; filename="arquivo.jpg"
                nm = re.search(r'name="(?P<name>[^"]+)"', h)
                if nm:
                    name = nm.group('name')
                fn = re.search(r'filename="(?P<fn>[^"]*)"', h)
                if fn:
                    filename = fn.group('fn')
                break
        if not name:
            continue
        if filename is not None:
            fields[name] = {'filename': filename, 'content': content}
        else:
            # decode text field
            fields[name] = content.decode('utf-8', errors='replace')
    return fields


class DenunciaHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print("%s - - [%s] %s" % (self.client_address[0], self.log_date_time_string(), format % args))

    def do_OPTIONS(self):
        try:
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()
        except Exception as e:
            print(f"Erro em do_OPTIONS: {e}")

    def do_GET(self):
        try:
            if self.path == "/" or self.path == "":
                self.path = "/index.html"
            return super().do_GET()
        except Exception as e:
            print(f"Erro em do_GET: {e}")
            traceback.print_exc()
            try:
                self.send_error(500, "Erro interno do servidor")
            except:
                pass

    def do_POST(self):
        if self.path != "/submit-denuncia":
            try:
                self.send_error(404, "Página não encontrada")
            except:
                pass
            return

        try:
            content_type = self.headers.get("Content-Type", "")
            try:
                content_length = int(self.headers.get("Content-Length", 0))
            except (ValueError, TypeError):
                content_length = 0

            # Limita tamanho máximo para 50MB
            if content_length > 52428800:
                enviar_resposta(
                    self,
                    {"success": False, "message": "Arquivo muito grande. Máximo 50MB."},
                    status=413,
                )
                return

            body = b""
            if content_length > 0:
                try:
                    body = self.rfile.read(content_length)
                except Exception as e:
                    print(f"Erro ao ler body: {e}")
                    enviar_resposta(
                        self,
                        {"success": False, "message": "Erro ao ler dados do formulário."},
                        status=400,
                    )
                    return

            # Parse form data (multipart/form-data or application/x-www-form-urlencoded)
            fields = {}
            ct_main = content_type.split(";", 1)[0].strip().lower()
            if ct_main == "multipart/form-data":
                fields = _parse_multipart(body, content_type)
            elif ct_main == "application/x-www-form-urlencoded":
                try:
                    qs = urllib.parse.parse_qs(body.decode("utf-8", errors="replace"), keep_blank_values=True)
                    # pegar primeiro valor de cada campo
                    fields = {k: v[0] if v else "" for k, v in qs.items()}
                except Exception as e:
                    print(f"Erro ao parsear form-urlencoded: {e}")
                    fields = {}
            else:
                fields = {}

            nome = (fields.get("nome") or "").strip()
            contato = (fields.get("contato") or "").strip()
            local = (fields.get("local") or "").strip()
            descricao = (fields.get("descricao") or "").strip()

            if not local or not descricao:
                enviar_resposta(
                    self,
                    {"success": False, "message": "Os campos Local e Descrição são obrigatórios."},
                    status=400,
                )
                return

            foto_path = None
            foto_field = fields.get("foto")
            if isinstance(foto_field, dict) and foto_field.get("filename"):
                try:
                    filename = Path(foto_field.get("filename")).name
                    safe_filename = re.sub(r"[^A-Za-z0-9_.-]", "_", filename)[:200]
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    target = UPLOADS_DIR / f"{timestamp}_{safe_filename}"
                    with open(target, "wb") as arquivo:
                        arquivo.write(foto_field.get("content") or b"")
                    foto_path = str(target.name)
                except Exception as e:
                    print(f"Erro ao salvar arquivo: {e}")
                    traceback.print_exc()
                    enviar_resposta(self, {"success": False, "message": f"Erro ao salvar o arquivo de imagem."}, status=500)
                    return

            try:
                salvar_denuncia(nome, contato, local, descricao, foto_path)
                enviar_resposta(self, {"success": True, "message": "Denúncia registrada com sucesso."})
            except Exception as erro:
                print(f"Erro ao salvar denuncia: {erro}")
                traceback.print_exc()
                enviar_resposta(
                    self,
                    {"success": False, "message": "Erro ao salvar a denúncia."},
                    status=500,
                )
        except Exception as e:
            print(f"Erro geral em do_POST: {e}")
            traceback.print_exc()
            try:
                enviar_resposta(
                    self,
                    {"success": False, "message": "Erro interno do servidor."},
                    status=500,
                )
            except:
                pass


if __name__ == "__main__":
    porta = 8000
    
    # Registra o handler para Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 60)
    print("SOS 102 - Servidor de Denúncias Ambientais")
    print("=" * 60)
    print(f"Iniciando servidor em http://localhost:{porta}")
    print("Pressione Ctrl+C para desligar o servidor")
    print("=" * 60)
    print()
    
    while True:
        try:
            globals()['servidor_global'] = ThreadingHTTPServer(("", porta), DenunciaHandler)
            servidor_global.serve_forever()
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"\n⚠️  Porta {porta} já está em uso!")
                print("Aguardando 3 segundos antes de tentar novamente...")
                time.sleep(3)
            else:
                print(f"\n❌ Erro: {e}")
                time.sleep(5)
        except Exception as e:
            print(f"\n❌ Erro no servidor: {e}")
            traceback.print_exc()
            time.sleep(5)
        finally:
            try:
                if servidor_global:
                    servidor_global.server_close()
            except:
                pass
