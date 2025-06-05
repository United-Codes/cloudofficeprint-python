import sys
sys.path.insert(0,"PATH_TO_COP_DIR")
import cloudofficeprint as cop

# Create main data structure representing the files array
files = cop.elements.ElementCollection(name="files")

# Create a file entry
file_entry = cop.elements.ElementCollection()
file_entry.add(cop.elements.Property("filename", "file1"))

# Add customer data
data_array = cop.elements.ElementCollection()
customer = cop.elements.Property(
    name='cust_first_name',
    value='John'
)
customer_last_name = cop.elements.Property(
    name='cust_last_name',
    value='Dullas'
)

data_array.add(customer)
data_array.add(customer_last_name)

# Product data
product1 = cop.elements.ElementCollection.from_mapping({
    "product_name": "Buisness Shirt",
    "unit_price": 50, 
    "quantity": 3,
    "category": "Mens"
})

product2 = cop.elements.ElementCollection.from_mapping({
    "product_name": "Trousers",
    "unit_price": 80,
    "quantity": 3,
    "category": "Mens" 
})

product3 = cop.elements.ElementCollection.from_mapping({
    "product_name": "Jacket", 
    "unit_price": 150,
    "quantity": 3,
    "category": "Mens"
})
product4 = cop.elements.ElementCollection.from_mapping({
    "product_name": "Blouse", 
    "unit_price": 60,
    "quantity": 3,
    "category": "Womens"
})
product5 = cop.elements.ElementCollection.from_mapping({
    "product_name": "Skirt", 
    "unit_price": 80,
    "quantity": 3,
    "category": "Womens"
})
product6 = cop.elements.ElementCollection.from_mapping({
    "product_name": "Ladies Shoes", 
    "unit_price": 120,
    "quantity": 2,
    "category": "Womens"
})
product7 = cop.elements.ElementCollection.from_mapping({
    "product_name": "Belt", 
    "unit_price": 50,
    "quantity": 2,
    "category": "Accessories"
})
product8 = cop.elements.ElementCollection.from_mapping({
    "product_name": "Bag", 
    "unit_price": 50,
    "quantity": 2,
    "category": "Accessories"
})
product9 = cop.elements.ElementCollection.from_mapping({
    "product_name": "Mens Shoes", 
    "unit_price": 110,
    "quantity": 2,
    "category": "Mens"
})
product10 = cop.elements.ElementCollection.from_mapping({
    "product_name": "Wallet", 
    "unit_price": 50,
    "quantity": 2,
    "category": "Accessories"
})

product = cop.elements.ForEach("product", [product1, product2, product3, product4, product5, product6, product7, product8, product9, product10])
data_array.add(product)

# Create main data object
main_data = cop.elements.ElementCollection()
main_data.add(cop.elements.Property("data", data_array))
data = main_data.as_dict

# Transformation function
js_code ="function generateProductRows(products, category) {\r\n    return products\r\n        .filter(product => product.category === category)\r\n        .map(product => {\r\n            if (category === \"Mens\") {\r\n                product.category_bold = \"true\";\r\n                product.product_name_font_color = \"blue\";\r\n            } else {\r\n                product.category_italic = \"true\";\r\n                product.product_name_font_color = \"red\";\r\n            }\r\n            const totalCost = product.unit_price * product.quantity;\r\n            return `\r\n                <tr>\r\n                    <td style=\"border-width: 1px; border-style: solid; border-color: black; padding: 8px;\">${product.product_name}</td>\r\n                    <td style=\"border-width: 1px; border-style: solid; border-color: black; padding: 8px;\">${product.unit_price}</td>\r\n                    <td style=\"border-width: 1px; border-style: solid; border-color: black; padding: 8px;\">${product.quantity}</td>\r\n                    <td style=\"border-width: 1px; border-style: solid; border-color: black; padding: 8px;\">${totalCost}</td>\r\n                </tr>\r\n            `;\r\n        })\r\n        .join('');\r\n}\r\n\r\nfunction transform() {\r\n    files.forEach(file => {\r\n        let data = file.data;\r\n            // Initialize HTML strings for mens_products and womens_products\r\n            let mensProductsHtml = '<table style=\"width: 100%; border: 2px solid blue; border-collapse: collapse;\">';\r\n            let womensProductsHtml = '<table style=\"width: 100%; border: 2px solid red; border-collapse: collapse;\">';\r\n\r\n            // Add table headers\r\n            const tableHeaders = `\r\n                <tr>\r\n                    <th style=\"border-width: 1px; border-style: solid; border-color: black; padding: 8px;\">Product Name</th>\r\n                    <th style=\"border-width: 1px; border-style: solid; border-color: black; padding: 8px;\">Unit Price</th>\r\n                    <th style=\"border-width: 1px; border-style: solid; border-color: black; padding: 8px;\">Quantity</th>\r\n                    <th style=\"border-width: 1px; border-style: solid; border-color: black; padding: 8px;\">Total Cost</th>\r\n                </tr>\r\n            `;\r\n            mensProductsHtml += tableHeaders;\r\n            womensProductsHtml += tableHeaders;\r\n\r\n            // Generate HTML rows for mens and womens products\r\n            const mensProductsRows = generateProductRows(data.product, \"Mens\");\r\n            const womensProductsRows = generateProductRows(data.product, \"Womens\");\r\n\r\n            // Calculate totals using reduce\r\n            const mensTotals = data.product\r\n                .filter(product => product.category === \"Mens\")\r\n                .reduce((totals, product) => {\r\n                    totals.quantity += product.quantity;\r\n                    totals.cost += product.unit_price * product.quantity;\r\n                    return totals;\r\n                }, { quantity: 0, cost: 0 });\r\n\r\n            const womensTotals = data.product\r\n                .filter(product => product.category === \"Womens\")\r\n                .reduce((totals, product) => {\r\n                    totals.quantity += product.quantity;\r\n                    totals.cost += product.unit_price * product.quantity;\r\n                    return totals;\r\n                }, { quantity: 0, cost: 0 });\r\n\r\n            // Close the HTML tables\r\n            mensProductsHtml += mensProductsRows + '</table>';\r\n            womensProductsHtml += womensProductsRows + '</table>';\r\n\r\n            // Add the new entries to the data object\r\n            data.mens_products = mensProductsHtml;\r\n            data.womens_products = womensProductsHtml;\r\n            data.mens_total_quantity = mensTotals.quantity;\r\n            data.mens_total_cost = mensTotals.cost;\r\n            data.womens_total_quantity = womensTotals.quantity;\r\n            data.womens_total_cost = womensTotals.cost;\r\n    });\r\n    return files;\r\n}\r\n"
# Transformation objeect
transformation_function = cop.TransformationFunction(js_code)

# transformation_function = cop.TransformationFunction("sample_transform.js")

# Configure the Server 
server = cop.config.Server(
    url="http://localhost:8010/",
    config=cop.config.ServerConfig(api_key="YOUR_API_KEY")  
)

template = cop.Resource.from_local_file(
    "./data/template.docx"
)
output_conf = cop.config.OutputConfig(filetype="pdf")

# Create print job 
printjob = cop.PrintJob(
    data=data,
    server=server,
    template=template,
    output_config=output_conf,
    transformation_function=transformation_function 
)

response = printjob.execute()
response.to_file(
        "./output/output.pdf")