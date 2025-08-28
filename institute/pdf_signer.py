from pyhanko.sign import signers
from pyhanko.sign.fields import SigFieldSpec
from pyhanko.sign.general import SigningError
from pyhanko.sign.signers.pdf_signer import PdfSigner
from pyhanko.stamp import TextStampStyle
from pyhanko.sign.signers.pdf_signer import PdfSignatureMetadata
from io import BytesIO
import os

def sign_pdf_with_p12(pdf_bytes, pkcs12_path, password=None, reason=None, location=None):
    """
    Firma un PDF en memoria usando un archivo .p12 y pyHanko

    param pdf_bytes: Los bytes del PDF a firmar
    param pkcs12_path: Ruta del archivo .p12
    param password: Contraseña del archivo .p12
    param reason: Razon de la firma
    param location: Ubicacion de la firma
    return; los bytes del PDF firmado
    """

    print("Ruta completa:", pkcs12_path)
    print("¿Existe el archivo?", os.path.exists(pkcs12_path))

    #crear el firmante desde el .p12 (Signer)
    signer = signers.SimpleSigner.load_pkcs12(pkcs12_path, password)
    print("Firmante cargado:", signer)

    #configurar el metadata y el estilo de la firma
    signature_meta = PdfSignatureMetadata(
        field_name='MiFirmaVisible', #nombre del cuerpo de la firma
        reason=reason,
        location=location
    )

    #estilo visual de la firma
    stamp_style = TextStampStyle(
        stamp_text="Firmado por MiFirmaDePrueba",
        background=None, #solo texto
        border_width=0, #sin borde visible
        text_box_style={"font-size": 10}
    )

    #POSICION del campo de la firma (visible)
    sig_field_spec = SigFieldSpec(
        sig_field_name="MiFirmaVisible",
        on_page=-1, #firma en la ultima pagina
        box=(50, 50, 250, 100) #(x1, y1, x2, y2)
    )

    #firmar en memoria
    input_buffer = BytesIO(pdf_bytes)
    input_buffer.seek(0)
    output_buffer = BytesIO()

    pdf_signer = PdfSigner(signature_meta, signer, stamp_style=stamp_style, new_field_spec=sig_field_spec)
    pdf_signer.sign_pdf(input_buffer, output_buffer)


    return output_buffer.getvalue()