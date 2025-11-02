# 🚨 INSTRUÇÕES URGENTES - Configure no Vercel Dashboard

## Passo 1: Configurar Variável de Ambiente no Vercel

1. Acesse: https://vercel.com/ana-luiza-guimaraes-luizaos-projects/bio-acess/settings/environment-variables

2. Adicione esta variável:
   ```
   Key: VITE_API_URL
   Value: /api
   Environments: Production, Preview, Development (marcar TODOS)
   ```

3. Clique em **Save**

---

## Passo 2: Forçar Redeploy

1. Vá em: https://vercel.com/ana-luiza-guimaraes-luizaos-projects/bio-acess/deployments

2. No último deployment, clique nos **3 pontinhos** → **Redeploy**

3. Marque **"Use existing Build Cache"** = NÃO (desmarcado)

4. Clique em **Redeploy**

---

## Passo 3: Limpar Cache do Browser

Depois que o deploy terminar:

1. Abra https://bio-acess.vercel.app
2. Pressione **Ctrl + Shift + Delete**
3. Limpe "Cached images and files"
4. Pressione **Ctrl + F5** para hard refresh

---

## ✅ Como Verificar se Funcionou

Abra DevTools (F12) → Console, você deve ver:

```
🔍 Debug Environment Variables: {
  VITE_API_URL: "/api",
  hostname: "bio-acess.vercel.app",
  API_BASE: "/api"
}
```

Se ver isso, está funcionando! ✅

---

**CRÍTICO:** A variável `VITE_API_URL` PRECISA estar no Dashboard do Vercel, não em arquivos!
