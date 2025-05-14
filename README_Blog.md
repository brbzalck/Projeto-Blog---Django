# 📝 Projeto Blog - Django

Este é um projeto de blog desenvolvido com o framework Django, com o objetivo de aplicar conceitos fundamentais e avançados da criação de aplicações web completas utilizando Python e Django.

## 🚀 Funcionalidades

- Criação e gerenciamento de posts
- Categorias e tags com URLs amigáveis
- Sistema de páginas dinâmicas (CMS simples)
- Filtro de busca com `Q` para pesquisas por título ou conteúdo
- Interface administrativa personalizada
- Upload, redimensionamento e otimização de imagens com Pillow
- Layout responsivo com HTML e CSS personalizado
- Editor HTML rico com django-summernote
- Slugs automáticos para URLs amigáveis
- Docker e Docker Compose para ambiente de desenvolvimento isolado
- Segurança com `django-axes`
- Configuração via `.env` usando `python-dotenv`

## 🧰 Tecnologias Utilizadas

- Python 3.12+
- Django 5.0+
- SQLite (para testes locais)
- HTML5 + CSS3
- Docker / Docker Compose
- Pillow
- django-summernote
- python-dotenv
- django-axes

## 📦 Instalação com Docker (recomendado)

1. Clone o repositório:
   ```bash
   git clone https://github.com/brbzalck/Projeto-Blog---Django.git
   cd Projeto-Blog---Django
   ```

2. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```

3. Suba os containers:
   ```bash
   docker-compose up --build
   ```

4. Acesse:
   ```
   http://localhost:8000
   ```

## 🧪 Usuário admin (exemplo)

Você pode criar um superusuário com:

```bash
docker-compose exec web python manage.py createsuperuser
```

## 📂 Estrutura de Diretórios

```text
Projeto-Blog---Django/
├── blog/                  # App principal com posts, tags e categorias
├── site_setup/           # Configurações de menu, favicon, etc.
├── core/                 # Configurações globais do projeto Django
├── media/                # Uploads de imagens
├── static/               # Arquivos estáticos (CSS, JS)
├── templates/            # Templates HTML
├── Dockerfile
├── docker-compose.yml
├── .env
└── requirements.txt
```

## 📚 Aprendizados

Durante o desenvolvimento deste projeto, aprofundei conhecimentos em:

- Class Based Views (`ListView`, `DetailView`)
- Templates Django e Context Processors
- Integração com Docker e variáveis de ambiente
- Boas práticas com o Admin do Django
- Modelagem com relacionamentos (`ForeignKey`, `ManyToManyField`)
- Redimensionamento e otimização de imagens
- Uso de `slugify`, `get_absolute_url`, `QuerySet` customizado

## 🛡️ Licença

Este projeto está sob a licença MIT.

---

🔗 [Me siga no LinkedIn](https://www.linkedin.com/in/seu-usuario/) para acompanhar meus próximos projetos e minha jornada de aprendizado com Python e Django!
