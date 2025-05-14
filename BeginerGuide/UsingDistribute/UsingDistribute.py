import sys
sys.path.insert(0, "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python")
import cloudofficeprint as cop

#ROOT element collection 
root = cop.elements.ElementCollection("root")

# Create file entry with filename
file_entry = cop.elements.ElementCollection.from_mapping({
    "filename": "department_report.docx"
})

# Main data container
data_content = cop.elements.ElementCollection("data")

# Create department elements 
def create_department(name, employees):
    dept = cop.elements.ElementCollection.from_mapping({
        "department": name 
    })
    dept.add(cop.elements.ForEach("employees", employees))
    return dept

# Create departments with distribution
departments = cop.elements.ForEachInline(
    name="departments",
    content=[
        create_department("Engineering", [
            cop.elements.ElementCollection.from_mapping({
                "name": "John Smith",
                "project": "Website Redesign",
                "status": "In Progress"
            }),
            cop.elements.ElementCollection.from_mapping({
                "name": "Emily Johnson",
                "project": "API Development",
                "status": "Completed"
            })
        ]),
        create_department("Marketing", [
            cop.elements.ElementCollection.from_mapping({
                "name": "Sarah Wilson",
                "project": "Brand Campaign",
                "status": "In Progress"
            }),
            cop.elements.ElementCollection.from_mapping({
                "name": "David Thompson",
                "project": "Market Research",
                "status": "Not Started"
            })
        ])
    ],
    distribute=True
)

# Build the hierarchy correctly
data_content.add(departments)
file_entry.add(data_content)
root.add(file_entry)

# Configure server
server = cop.config.Server("http://localhost:8010/")

# Create print job with CORRECT OUTPUT PATH
printjob = cop.PrintJob(
    data=root,
    server=server,
    template=cop.Resource.from_local_file(
        "C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python/BeginerGuide/UsingDistribute/data/horizontal_tabular_looping_output-ed506eb2e341afbf52e1a05319e2b086.docx"
    ),
)

# Save to DIFFERENT FILE than template
response = printjob.execute()
response.to_file("C:/Users/em8ee/OneDrive/Documents/cloudofficeprint-python/BeginerGuide/UsingDistribute/output/output.docx")