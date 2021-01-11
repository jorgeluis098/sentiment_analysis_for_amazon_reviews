These models are for general Amazon web scraping. 
That is why through the main amazon page, a tree is created that can be navigated to find products from different departments, categories, etc.
The structure is :

Department:
    Category:
        Product Category:
            Product Page:
                Product: 
                    Review:  

e.g.
Alimentos y Bebidas:
    Alimentos:
        Aceites, Vinagres y Aderezos:
            https://www.amazon.com.mx/s?rh=n%3A17724549011&fs=true&ref=lp_17724549011_sar
                1-2-3 Aceite Vegetal,1 Lt
                Capullo Aceite de Canola, 840 ml
                Bragg - Vinagre de Manzana Orgánico 473ml
                .
                .
                .
        Arroz, Frijoles y Pasta
        Botanas y Dulces
        Café, Té y Bebidas
        Canastas de Regalo y Regalos Gourmet
        .
        .
        .
    Cervezas, Vinos y Licores:
        Bebidas y Cocteles Premezclados
        Cervezas
        Bebidas Espiritosas
        Sakes y Licores de Arroz
        .
        .
        .


########################################
############ IMPORTANT #################
########################################

Each class related to the product has as main components:
Name        : Name of product, department, category etc. This is for any search
url         : URL from href, this is a relative URL
base url    : Base url to concatenate with url above. Now is amazon.com.mx but it might work for other amazon stores.
