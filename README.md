# 🌍 SOS 102 - Servidor de Denúncias Ambientais

## 📋 Informações Importantes

O servidor agora está **otimizado para rodar 24/7** sem travamentos!

## ⚙️ Como Iniciar o Servidor

Você tem 3 opções para manter o servidor rodando continuamente:

### Opção 1: Script Python (RECOMENDADO) ⭐
Mais confiável e com suporte total a reinicializações automáticas.

```bash
python gerenciador_servidor.py
```

Este script:
- ✅ Mantém o servidor rodando 24/7
- ✅ Reinicia automaticamente em caso de erro
- ✅ Mostra logs em tempo real
- ✅ Trata travamentos e exceções

### Opção 2: Script Batch (Windows)
Simples mas com reinicializações automáticas.

```bash
iniciar_servidor.bat
```

### Opção 3: Direto com Python
Para desenvolvimento e testes:

```bash
python server.py
```

---

## 🌐 Acessar o Sistema

Após iniciar o servidor, abra no navegador:

**Página de Denúncia:** http://localhost:8000/

**Mapa de Ocorrências:** http://localhost:8000/mapa.html

---

## 🔧 Melhorias Implementadas

### Servidor Python (server.py)
- ✅ Tratamento robusto de erros em todas as operações
- ✅ Limite de tamanho de arquivo (50MB máximo)
- ✅ Timeouts configuráveis
- ✅ Logs detalhados de todas as ações
- ✅ Reinicialização automática em caso de falha
- ✅ Suporte a requisições OPTIONS para CORS
- ✅ Validação rigorosa de entrada

### Frontend (index.html)
- ✅ Melhor tratamento de erros de conexão
- ✅ Timeout de 30 segundos para requisições
- ✅ Feedback visual durante o envio
- ✅ Detecção automática do servidor online/offline
- ✅ Mensagens de erro mais claras
- ✅ Desabilitação de botão durante envio

---

## 📊 Verificação de Status

Para verificar se tudo está funcionando:

1. Abra http://localhost:8000/ no navegador
2. Verifique se a página carrega corretamente
3. Teste o formulário com dados fictícios
4. Verifique a pasta `uploads/` para confirmar que as fotos foram salvas
5. Abra `denuncias.txt` para ver os registros

---

## 🛑 Parar o Servidor

Pressione **Ctrl+C** no terminal onde o servidor está rodando.

Se estiver usando o gerenciador Python, ele encerra de forma segura.

---

## 📁 Arquivos Importantes

- `server.py` - Servidor HTTP (melhorado)
- `gerenciador_servidor.py` - Gerenciador 24/7 (novo)
- `iniciar_servidor.bat` - Script batch de inicialização (novo)
- `index.html` - Página de denúncia (melhorada)
- `denuncias.txt` - Arquivo com todas as denúncias
- `uploads/` - Pasta com as fotos enviadas

---

## 🆘 Solução de Problemas

### Porta 8000 já está em uso
```
Erro: Address already in use
```
**Solução:** Mude a porta em `server.py` (linha com `porta = 8000`) para outra disponível.

### Conexão recusada
```
Erro: Connection refused
```
**Solução:** Certifique-se de que o servidor está rodando. Use `gerenciador_servidor.py` para deixá-lo sempre online.

### Arquivo corrompido ou permissões
**Solução:** Execute o terminal como Administrador.

### Servidor desconecta frequentemente
**Solução:** Use o `gerenciador_servidor.py` que reinicia automaticamente.

---

## 📞 Suporte

Para mais informações, verifique os logs do servidor (aparecem no terminal).

**Turma 102 de Internet - 2026**
