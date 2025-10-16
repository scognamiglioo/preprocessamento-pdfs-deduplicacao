def preprocess_text(self, text: str) -> str:
        """
        Normalização do texto para deduplicação:
        - Minúsculas, remoção de pontuação, etc.
        """
        if not text:
            return ""

        # converter para minúsculas
        text = text.lower()

        # expandir siglas
        for sigla, expansao in self.siglas.items():
            text = re.sub(rf'\b{sigla}\b', expansao.lower(), text, flags=re.IGNORECASE)

        # normalizar caracteres (remover acentos)
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

        # remover pontuação e caracteres especiais
        text = re.sub(r'[^\w\s]', ' ', text)

        # padronizar formato de artigos e parágrafos
        text = re.sub(r'artigo\s+(\d+)', r'art \1', text)
        text = re.sub(r'art\.?\s*(\d+)', r'art \1', text)
        text = re.sub(r'parágrafo\s+único', 'paragrafo unico', text)
        text = re.sub(r'§\s*(\d+)', r'paragrafo \1', text)

        # remover espaços extras e normalizar
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def clean_text(self, text: str) -> str:
        """
        Limpeza básica do texto para deduplicação
        """
        if not text:
            return ""

        # remover espaços extras e normalizar quebras
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def deduplicate_pages(self, pages_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove páginas duplicadas ou muito similares
        """

        if len(pages_data) <= 1:
            return pages_data

        # deduplicação exata
        unique_pages = self._remove_exact_duplicates(pages_data)
        print(f"  Fase 1 - Duplicatas exatas: {len(pages_data) - len(unique_pages)} removidas")

        # deduplicação por similaridade
        final_pages = self._remove_similar_pages(unique_pages)
        print(f"  Fase 2 - Páginas similares: {len(unique_pages) - len(final_pages)} removidas")

        return final_pages

    def _remove_exact_duplicates(self, pages_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove páginas com conteúdo exatamente igual"""
        unique_pages = []
        seen_hashes = set()

        for page in pages_data:
            # criar hash do conteúdo normalizado
            content_hash = hashlib.md5(page['normalized_text'].encode()).hexdigest()

            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique_pages.append(page)
            else:
                print(f" Removendo página {page['page']} (duplicata exata)")

        return unique_pages

    def _remove_similar_pages(self, pages_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove páginas com conteúdo muito similar"""
        if len(pages_data) <= 1:
            return pages_data

        # extrair textos para comparação
        texts = [page['normalized_text'] for page in pages_data]

        # usar TF-IDF e similaridade de cosseno
        vectorizer = TfidfVectorizer(min_df=1, max_df=0.9)
        try:
            tfidf_matrix = vectorizer.fit_transform(texts)
            cosine_sim = cosine_similarity(tfidf_matrix)

            to_keep = set(range(len(pages_data)))

            for i in range(len(pages_data)):
                if i in to_keep:
                    for j in range(i + 1, len(pages_data)):
                        if j in to_keep and cosine_sim[i][j] >= self.similarity_threshold:
                            to_keep.remove(j)
                            print(f"  Removendo página {pages_data[j]['page']} "
                                  f"(similar à página {pages_data[i]['page']})")

            return [pages_data[i] for i in sorted(to_keep)]

        except Exception as e:
            print(f"  Erro na deduplicação fuzzy: {e}")

            return pages_data  # Retorna todas se houver erro
