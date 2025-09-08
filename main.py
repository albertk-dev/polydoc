import pypandoc
import uuid
import os
import json
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

# ==============================================================================
# 1. SETUP DE L'APPLICATION
# ==============================================================================

TMP_DIR = "temp_files"
if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

app = FastAPI(
    title="PolyDoc API",
    description="Un service pour générer des documents PDF et DOCX à partir de Markdown.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# 2. SCHÉMAS PYDANTIC (Modifiés pour inclure le contenu)
# ==============================================================================

class MarginOptions(BaseModel):
    top: Optional[str] = Field("2cm", description="Marge du haut (ex: '2cm', '1in')")
    bottom: Optional[str] = Field("2cm", description="Marge du bas (ex: '2cm', '1in')")
    left: Optional[str] = Field("2.5cm", description="Marge de gauche (ex: '2.5cm', '1in')")
    right: Optional[str] = Field("2.5cm", description="Marge de droite (ex: '2.5cm', '1in')")


class MetadataOptions(BaseModel):
    title: Optional[str] = Field(None, description="Titre du document")
    author: Optional[str] = Field(None, description="Auteur du document")


class ConversionOptions(BaseModel):
    metadata: Optional[MetadataOptions] = Field(None, description="Métadonnées du document (titre, auteur)")
    toc: Optional[bool] = Field(False, description="Génère une Table des Matières")
    lof: Optional[bool] = Field(False, description="Génère une Liste des Figures")
    margins: Optional[MarginOptions] = Field(default_factory=MarginOptions, description="Marges de la page")
    orientation: Optional[str] = Field("portrait", description="Orientation : 'portrait' ou 'landscape'")
    fontSize: Optional[int] = Field(12, description="Taille de la police principale en points")
    fontFamily: Optional[str] = Field(None, description="Famille de la police principale (ex: 'Lato')")


class GenerationRequest(BaseModel):
    content: str = Field(..., description="Contenu Markdown brut du document.")
    options: ConversionOptions = Field(default_factory=ConversionOptions,
                                       description="Options de conversion et de style.")


# ==============================================================================
# 3. ENDPOINTS DE L'API (Simplifiés)
# ==============================================================================

@app.get("/")
def read_root():
    return {"message": "PolyDoc Service is running. Go to /docs for API documentation."}


@app.post("/generate/{doc_format}")
async def generate_document(
        doc_format: str,
        request: GenerationRequest
):
    """
    Génère un document (PDF ou DOCX) à partir d'un corps de requête JSON.
    """
    if doc_format not in ["pdf", "docx"]:
        raise HTTPException(status_code=404, detail="Format not supported. Use 'pdf' or 'docx'.")

    output_filename = os.path.join(TMP_DIR, f"{uuid.uuid4()}.{doc_format}")
    extra_args = []

    # On accède maintenant aux options via request.options
    options = request.options

    if options.metadata:
        if options.metadata.title: extra_args.extend(['--metadata', f'title={options.metadata.title}'])
        if options.metadata.author: extra_args.extend(['--metadata', f'author={options.metadata.author}'])

    if doc_format == 'pdf':
        extra_args.append('--pdf-engine=lualatex')
        # Force le placement des images à l'endroit exact où elles sont dans le Markdown
        # H majuscule signifie "HERE!"
        # VERSION CORRIGÉE : On s'assure que le code est bien formaté
        header_includes = r"""
        \usepackage{float}
        \floatplacement{figure}{H}
        """
        extra_args.extend(['--variable', f'header-includes:{header_includes}'])
        if options.orientation == 'landscape':
            extra_args.extend(['--variable', 'geometry:landscape'])

    if options.toc: extra_args.append('--toc')
    if options.lof: extra_args.extend(['--variable=lof'])

    if options.margins:
        if options.margins.top: extra_args.extend(['--variable', f'geometry:top={options.margins.top}'])
        if options.margins.bottom: extra_args.extend(['--variable', f'geometry:bottom={options.margins.bottom}'])
        if options.margins.left: extra_args.extend(['--variable', f'geometry:left={options.margins.left}'])
        if options.margins.right: extra_args.extend(['--variable', f'geometry:right={options.margins.right}'])

    if options.fontSize: extra_args.extend(['--variable', f'fontsize={options.fontSize}pt'])
    if options.fontFamily: extra_args.extend(['--variable', f'mainfont={options.fontFamily}'])

    try:
        pypandoc.convert_text(
            source=request.content,  # On utilise request.content
            to=doc_format,
            format='markdown',
            outputfile=output_filename,
            extra_args=extra_args
        )

        media_type = "application/pdf" if doc_format == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        return FileResponse(path=output_filename, media_type=media_type, filename=f"export.{doc_format}")
    except Exception as e:
        if os.path.exists(output_filename):
            os.remove(output_filename)
        raise HTTPException(status_code=500, detail=f"Pandoc error: {str(e)}")