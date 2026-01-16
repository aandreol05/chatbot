import os
import glob
from dotenv import load_dotenv
from upstash_vector import Index, Vector

# ---------------- CONFIG ----------------

load_dotenv(override=True)
index = Index.from_env()

DATA_DIR = "data"
# Ajustez la granularité via les variables d'env ou réduisez ici pour découper l'intérieur des fichiers
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 200))

# ---------------- HELPERS ----------------

def split_by_heading(text: str):
    """Découpe le contenu par sections Markdown (lignes qui commencent par #)."""
    sections = []
    current = []

    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("#") and current:
            sections.append("".join(current).strip())
            current = []
        current.append(line)

    if current:
        sections.append("".join(current).strip())

    return [s for s in sections if s]


def chunk_text(text: str):
    """Découpe par section (#) puis par blocs de CHUNK_SIZE sans overlap."""
    chunks = []
    for section in split_by_heading(text):
        start = 0
        while start < len(section):
            chunks.append(section[start:start + CHUNK_SIZE])
            start += CHUNK_SIZE
    return chunks


# ---------------- MAIN ----------------

vectors = []
vector_id = 0

for filepath in glob.glob(f"{DATA_DIR}/**/*.md", recursive=True):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = chunk_text(content)

    for i, chunk in enumerate(chunks):
        vectors.append(
            Vector(
                id=f"{os.path.basename(filepath)}-{vector_id}",
                data=chunk,  # ← Upstash génère l'embedding
                metadata={
                    "source": filepath,
                    "chunk": i,
                },
            )
        )

        vector_id += 1

# ---------------- UPSERT ----------------

index.upsert(vectors=vectors)

print(f"✅ {len(vectors)} chunks indexés avec succès")
