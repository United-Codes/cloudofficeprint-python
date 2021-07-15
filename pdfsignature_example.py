from apexofficeprint._utils import file_utils
import apexofficeprint as aop

# Setup AOP server
LOCAL_SERVER_URL = "http://localhost:8010"
API_KEY = "1C511A58ECC73874E0530100007FD01A"

server = aop.config.Server(
    LOCAL_SERVER_URL,
    aop.config.ServerConfig(api_key=API_KEY)
)


# Create empty element collection
collection = aop.elements.ElementCollection()


# Add pdf signature
pdf_options = aop.config.PDFOptions(
    sign_certificate=file_utils.read_file_as_base64('./pdfsignature_example/pkijs_pkcs12.p12')
)
conf = aop.config.OutputConfig(
    pdf_options=pdf_options
)


# Create printjob
printjob = aop.PrintJob(
    template=aop.Resource.from_local_file('./pdfsignature_example/pdfsignature_template.pdf'),
    data=collection,
    server=server,
    output_config=None
)


# Execute printjob
printjob.execute().to_file('./pdfsignature_example/output')