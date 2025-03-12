# Telegram AI Chatbot with OpenAI, Aiogram 3, and FastAPI

## 📌 Task Description

### **Тестовая задача: Разработка Telegram-бота с использованием OpenAI, Aiogram 3 и FastAPI**

Вам необходимо разработать Telegram-бота, который будет отвечать на различные вопросы и запросы пользователей, используя OpenAI (например, GPT-3.5). Бот должен вести диалоги с пользователями, запоминать историю общения и использовать её для генерации контекстных ответов. Также бот должен предоставлять возможность регистрации пользователей для персонализации взаимодействия и сохранения индивидуальной истории переписки.

Бот должен быть разделён на три независимых сервиса:

1. **Bot Service (Aiogram 3)**:

   - Регистрация и авторизация пользователей через Telegram.
   - Обработка входящих запросов и команд пользователей.
   - Взаимодействие с NLP-сервисом для получения сгенерированных ответов и отправка их пользователям.

2. **API Service (FastAPI)**:

   - REST API для управления пользователями (регистрация, авторизация, получение данных пользователей).
   - REST API для мониторинга и администрирования работы бота (статистика использования, контроль функциональности).

3. **NLP Service (OpenAI)**:
   - Интеграция с OpenAI API для обработки текстовых запросов.
   - Хранение и использование истории общения для генерации контекстных ответов с помощью языковой модели GPT.

---

## ✅ **Project Implementation**

This project follows a **modular architecture** with three independent services communicating via **REST API**.

### **Technologies Used**

- **Python 3.8+** (Main Language)
- **Aiogram 3** (Telegram Bot Framework)
- **FastAPI** (Backend API Service)
- **OpenAI GPT-3.5** (Natural Language Processing)
- **SQLite** (Database for user management & chat history)
- **Docker (Optional)** (For easy deployment)
- **Async Programming** (Using `aiohttp` for fast performance)

---

## 🚀 **How to Run the Project**

### **1️⃣ Install Dependencies**

First, install **Python 3.8+** and required dependencies:


### **2️⃣ Set Up Environment Variables**

Create a `.env` file in each service (`bot_service`, `api_service`, `nlp_service`):

**Example `.env` file:**

```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=sqlite:///./users.db
```

### **3️⃣ Start Each Service**

Run these in separate terminals:

- **Start API Service** (User Registration & Chat History)

  ```sh
  cd api_service
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
  ```

- **Start NLP Service** (OpenAI Chat Processing)

  ```sh
  cd nlp_service
  uvicorn main:app --host 0.0.0.0 --port 8001 --reload
  ```

- **Start Bot Service** (Telegram Bot)
  ```sh
  cd bot_service
  python3 bot.py
  ```

---

## 🎯 **Project Features**

### ✅ **Implemented Requirements**

| **Requirement**                                        | **Status** |
| ------------------------------------------------------ | ---------- |
| **Bot Service (Aiogram 3) working**                    | ✅ Done    |
| **API Service (FastAPI) handles users & chat history** | ✅ Done    |
| **NLP Service (OpenAI) generates responses**           | ✅ Done    |
| **All services communicate via HTTP (REST API)**       | ✅ Done    |
| **Asynchronous implementation**                        | ✅ Done    |
| **Messages are saved in the database**                 | ✅ Done    |
| **Users can retrieve chat history**                    | ✅ Done    |
| **Bot remembers conversation context**                 | ✅ Done    |
| **Proper error handling**                              | ✅ Done    |
| **Swagger API documentation (`/docs`)**                | ✅ Done    |
| **SOLID architecture used**                            | ✅ Done    |

---

## 📝 **How It Works**

1. **User sends a message** in Telegram.
2. **Bot registers user** in `api_service` if they are new.
3. **Message is saved** in `api_service` for future reference.
4. **Bot forwards message** to `nlp_service`, fetching **past chat history**.
5. **OpenAI processes the message** with full conversation context.
6. **Bot sends the AI-generated reply** back to the user.

---

## 🔥 **Additional Features**

- **Database-backed chat history** (Bot remembers context!)
- **Auto-reconnect & error handling** for stability.
- **REST API endpoints** for user data & chat monitoring.
- **Fast execution** using async programming.

