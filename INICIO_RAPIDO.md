# 🚀 GUIA RÁPIDO - SOS 102 SERVER 24/7

## ✅ O que foi corrigido e melhorado

### ✨ Servidor Python (server.py)
- ✅ **Tratamento robusto de erros** - Nenhuma exceção mais vai travar o servidor
- ✅ **Reinicialização automática** - Se o servidor cair, tenta reiniciar automaticamente
- ✅ **Limit de upload** - Máximo 50MB por arquivo
- ✅ **Timeouts configuráveis** - Evita travamentos por conexões lentas
- ✅ **Logs detalhados** - Ver exatamente o que está acontecendo
- ✅ **Melhor parsing de formulários** - Trata multipart e form-urlencoded
- ✅ **Handler graceful do Ctrl+C** - Encerra de forma segura

### 🎨 Frontend (index.html)
- ✅ **Melhor feedback do usuário** - Mostra mensagens de erro mais claras
- ✅ **Timeout de 30 segundos** - Não deixa o usuário esperando infinitamente
- ✅ **Desabilita botão durante envio** - Evita envios duplicados
- ✅ **Detecção automática do servidor** - Avisa se está offline
- ✅ **Tratamento de erros de conexão** - Mensagens específicas para cada tipo de erro

### 🔧 Novos scripts

#### 1. **gerenciador_servidor.py** ⭐ RECOMENDADO
- Mantém o servidor rodando 24/7
- Reinicia automaticamente em caso de erro
- Mostra logs em tempo real
- Melhor controle e confiabilidade

#### 2. **iniciar_servidor.bat**
- Atalho fácil para Windows
- Pode ser colocado na Barra de Tarefas
- Duplo clique para iniciar

---

## 🎯 COMO USAR - 3 PASSOS SIMPLES

### Passo 1: Escolha sua opção

**OPÇÃO A (Recomendada):**
```bash
python gerenciador_servidor.py
```

**OPÇÃO B (Alternativa Windows):**
Duplo clique em `iniciar_servidor.bat`

**OPÇÃO C (Desenvolvimento):**
```bash
python server.py
```

### Passo 2: Abra no navegador
```
http://localhost:8000
```

### Passo 3: Use a plataforma!
- Registre denúncias
- Envie fotos
- Veja o mapa
- Acompanhe ocorrências

---

## 📋 ARQUIVOS IMPORTANTES

| Arquivo | Função |
|---------|--------|
| `server.py` | Servidor HTTP (melhorado) |
| `gerenciador_servidor.py` | Gerenciador 24/7 (NOVO) ⭐ |
| `iniciar_servidor.bat` | Atalho Windows (NOVO) |
| `index.html` | Página de denúncia (melhorada) |
| `mapa.html` | Mapa de ocorrências |
| `denuncias.txt` | Banco de dados de denúncias |
| `uploads/` | Fotos enviadas |

---

## 🆘 TROUBLESHOOTING

### Problema: "Address already in use"
**Solução:** A porta 8000 já está sendo usada
```bash
# Mude a porta em server.py:
# Procure por: porta = 8000
# Mude para: porta = 8001 (ou outra)
```

### Problema: "Connection refused"
**Solução:** O servidor não está rodando
```bash
# Use: python gerenciador_servidor.py
# Ele mantém o servidor sempre ligado
```

### Problema: "Tempo limite excedido"
**Solução:** Conexão lenta ou arquivo muito grande
- Verifique sua internet
- Reduza o tamanho das fotos
- Tente novamente

### Problema: Servidor desconecta frequentemente
**Solução:** Use o gerenciador
```bash
python gerenciador_servidor.py
```
Ele reinicia automaticamente!

---

## 💡 DICAS IMPORTANTES

### 1. Sempre use o Gerenciador (24/7)
```bash
python gerenciador_servidor.py
```
Deixe rodando sempre!

### 2. Para monitorar em tempo real
Veja o terminal - mostra todas as requisições e erros

### 3. Para acessar em outro PC na rede
```
http://SEU_IP:8000
# Exemplo: http://192.168.1.100:8000
```

### 4. Para fazer backup das denúncias
Copie o arquivo `denuncias.txt`
Copie a pasta `uploads/`

---

## ✅ CHECKLIST DE TESTES

- [ ] Servidor inicia sem erros
- [ ] Página carrega em `http://localhost:8000`
- [ ] Formulário aparecer
- [ ] Enviou uma denúncia de teste
- [ ] Arquivo foi salvo em `denuncias.txt`
- [ ] Foto foi salva em `uploads/`
- [ ] Mapa carrega corretamente

---

## 📞 SUPORTE

Verifique os logs no terminal para diagnosticar problemas.

**Desenvolvido pela Turma 102 de Internet - 2026**
