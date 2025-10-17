# Deduplicação de Texto 

Este projeto implementa um sistema completo de **deduplicação de texto** — desde o pré-processamento até a análise semântica — ideal para eliminar redundâncias em grandes volumes de dados textuais.


---

## Funcionalidades

-  **Extração de texto** de documentos PDF (`pdfplumber`, `PyPDF2`)
-  **Pré-processamento** e normalização textual
-  **Deduplicação exata** (comparação direta)
-  **Deduplicação fuzzy/semântica** usando:
  - Similaridade de Cosseno: **TF-IDF embeddings**
-  **Exportação em JSON** dos resultados

---

## Estrutura
- `src/`: função em Python 
- `notebooks/`: função em Jupyter Notebook
- `data/input/`: documentos PDF de entrada
- `data/output/`: resultados gerados em JSON

---

## Tecnologias Utilizadas

| Biblioteca | Função |
|-------------|--------|
| `re`, `unicodedata` | Limpeza e normalização textual |
| `hashlib` | Hash para deduplicação exata |
| `difflib` | Cálculo da similaridade de edição |
| `sklearn.feature_extraction.text.TfidfVectorizer` | Criação de embeddings |
| `sklearn.metrics.pairwise.cosine_similarity` | Medição de similaridade semântica |
| `numpy` | Manipulação vetorial |
| `pdfplumber` / `PyPDF2` | Extração de texto de PDFs |
| `dataclasses` | Estruturação de dados do sistema |

---

## Etapas do Processo

### Pré-processamento

Todos os trechos passam por uma **normalização** antes da deduplicação:

- Conversão para **minúsculas**
- **Remoção de pontuação** e caracteres especiais
- **Remoção de acentos** (`unicodedata.normalize`)
- **Limpeza de espaços extras**


### Deduplicação Exata (Fase 1)

Após a normalização, trechos **idênticos** são removidos.

- Cada texto normalizado é convertido em um **hash**
- Hashes iguais indicam duplicatas
- Resultado: remoção eficiente e determinística

### Deduplicação Fuzzy / Semântica (Fase 2)

Para eliminar duplicatas **parecidas, mas não idênticas**, o sistema utiliza da seguinte abordagem:

#### 🔹 A. Similaridade de Cosseno (com TF-IDF Embeddings)

- Cada texto é vetorizado com **TF-IDF**  
- A **similaridade de cosseno** é calculada entre todos os vetores  
- Textos com similaridade acima de um **limiar (0.9)** são considerados duplicatas semânticas

