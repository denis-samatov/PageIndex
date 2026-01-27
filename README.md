<div align="center">
  
<a href="https://vectify.ai/pageindex" target="_blank">
  <img src="https://github.com/user-attachments/assets/46201e72-675b-43bc-bfbd-081cc6b65a1d" alt="Баннер PageIndex" />
</a>

<br/>
<br/>

<p align="center">
  <a href="https://trendshift.io/repositories/14736" target="_blank"><img src="https://trendshift.io/api/badge/repositories/14736" alt="VectifyAI%2FPageIndex | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>
</p>

# PageIndex: RAG без векторов на основе рассуждений

<p align="center"><b>RAG на основе рассуждений&nbsp; ◦ &nbsp;без векторной БД&nbsp; ◦ &nbsp;без чанков&nbsp; ◦ &nbsp;извлечение как у человека</b></p>

<h4 align="center">
  <a href="https://vectify.ai">🏠 Домашняя страница</a>&nbsp; • &nbsp;
  <a href="https://chat.pageindex.ai">🖥️ Чат-платформа</a>&nbsp; • &nbsp;
  <a href="https://pageindex.ai/mcp">🔌 MCP</a>&nbsp; • &nbsp;
  <a href="https://docs.pageindex.ai">📚 Документация</a>&nbsp; • &nbsp;
  <a href="https://discord.com/invite/VuXuf29EUj">💬 Discord</a>&nbsp; • &nbsp;
  <a href="https://ii2abc2jejf.typeform.com/to/tK3AXl8T">✉️ Контакты</a>&nbsp;
</h4>
  
</div>


<details open>
<summary><h3>📢 Последние обновления</h3></summary>

 **🔥 Релизы:**
- [**PageIndex Chat**](https://chat.pageindex.ai): Первая человекоподобная платформа агента для анализа документов, созданная для профессиональных длинных документов. Также доступна интеграция через [MCP](https://pageindex.ai/mcp) или [API](https://docs.pageindex.ai/quickstart) (бета).
 
 **📝 Статьи:**
- [**PageIndex Framework**](https://pageindex.ai/blog/pageindex-intro): Представляет фреймворк PageIndex — *агентный, in-context* *древовидный индекс*, который позволяет LLM выполнять *извлечение на основе рассуждений*, *похожее на человеческое*, по длинным документам без векторной БД и чанкинга.

 **🧪 Кукбуки:**
- [Vectorless RAG](https://docs.pageindex.ai/cookbook/vectorless-rag-pageindex): Минимальный практический пример RAG на основе рассуждений с использованием PageIndex. Без векторов, без чанков и с извлечением как у человека.
- [Vision-based Vectorless RAG](https://docs.pageindex.ai/cookbook/vision-rag-pageindex): RAG без OCR, только зрение; reasoning-native подход, который работает напрямую по изображениям страниц PDF.
</details>

---

# 📑 Введение в PageIndex

Вас не устраивает точность извлечения в векторных БД для длинных профессиональных документов? Традиционный векторный RAG опирается на семантическое *сходство*, а не на реальную *релевантность*. Но **сходство ≠ релевантность** — в извлечении нам нужна **релевантность**, а для нее требуется **рассуждение**. При работе с профессиональными документами, где важны доменные знания и многошаговое мышление, поиск по сходству часто не справляется.

Вдохновившись AlphaGo, мы предлагаем **[PageIndex](https://vectify.ai/pageindex)** — **RAG без векторов**, основанный на рассуждениях, который строит **иерархический древовидный индекс** из длинных документов и использует LLM, чтобы **рассуждать по этому индексу** для **агентного, контекстно-зависимого извлечения**.

---

# ⚙️ Использование пакета

### 1. Установите зависимости

```bash
pip3 install --upgrade -r requirements.txt
pip3 install -e .
```

### 2. Укажите API-ключ OpenAI

Создайте файл `.env` в корневой директории и добавьте ваш ключ API:

```bash
OPENAI_API_KEY=your_openai_key_here
```

### 3. Запустите PageIndex для вашего PDF

```bash
pageindex --pdf_path /path/to/your/document.pdf
```

---

# 💻 Developer Guide

This section is for developers contributing to `PageIndex` or integrating it as a library.

### Development Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/VectifyAI/PageIndex.git
    cd PageIndex
    ```

2.  **Install development dependencies:**
    ```bash
    pip install -e ".[dev]"
    # Or simply:
    pip install pytest pytest-asyncio
    ```

3.  **Run Tests:**
    We use `pytest` for unit and integration testing.
    ```bash
    pytest
    ```

### Project Structure

The project has been refuted into a modular library structure under `src/pageindex`.

-   `src/pageindex/core/`: Core logic modules.
    -   `llm.py`: LLM interactions and token counting.
    -   `pdf.py`: PDF text extraction and processing.
    -   `tree.py`: Tree data structure manipulation and recursion.
    -   `logging.py`: Custom logging utilities.
-   `src/pageindex/config.py`: Configuration loading and validation (Pydantic).
-   `src/pageindex/cli.py`: Command Line Interface entry point.
-   `src/pageindex/utils.py`: Facade for backward compatibility.

### Configuration

Configuration is handled via `src/pageindex/config.py`. You can modify default settings in `config.yaml` or override them via environment variables (`PAGEINDEX_CONFIG`) or CLI arguments.
Config validation is powered by Pydantic, ensuring type safety.

For API Reference, please see [API_REFERENCE.md](docs/API_REFERENCE.md).

---

# ⭐ Поддержите нас

Поставьте нам звезду 🌟, если вам нравится проект. Спасибо!
