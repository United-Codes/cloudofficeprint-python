import sys
sys.path.insert(0, "PATH_TO_COP_DIR")
import cloudofficeprint as cop 


data = cop.elements.ElementCollection("data")

eng_emp1 = cop.elements.ElementCollection.from_mapping({
    "name": "John Smith",
    "project": "Website Redesign", 
    "status": "In Progress"
})

eng_emp2 = cop.elements.ElementCollection.from_mapping({
    "name": "Emily Johnson",
    "project": "API Development",
    "status": "Completed"
})

eng_emp3 = cop.elements.ElementCollection.from_mapping({
    "name": "Michael Brown", 
    "project": "Mobile App",
    "status": "Planning"
})

mkt_emp1 = cop.elements.ElementCollection.from_mapping({
    "name": "Sarah Wilson",
    "project": "Brand Campaign",
    "status": "In Progress"
})

mkt_emp2 = cop.elements.ElementCollection.from_mapping({
    "name": "David Thompson",
    "project": "Market Research", 
    "status": "Not Started"
})

engineering_dept = cop.elements.ElementCollection.from_mapping({
    "department": "Engineering"
})
engineering_dept.add(cop.elements.ForEachMergeCells("employees", [eng_emp1, eng_emp2, eng_emp3]))

marketing_dept = cop.elements.ElementCollection.from_mapping({
    "department": "Marketing"
})
marketing_dept.add(cop.elements.ForEachMergeCells("employees", [mkt_emp1, mkt_emp2]))

departments = cop.elements.ForEachMergeCells("departments", [engineering_dept, marketing_dept])

data.add(departments)

server = cop.config.Server(
    "http://localhost:8010/"
)
# Create print job
# PrintJob combines template, data, server and an optional output configuration
printjob = cop.PrintJob(
    data=data,
    server=server,
    template=cop.Resource.from_local_file("./data/tem.docx"),
)
response = printjob.execute()
response.to_file("./output/output.docx")