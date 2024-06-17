import streamlit as st
import pandas as pd

file_path = 'TXzipcitycountycountycode.csv'
df = pd.read_csv(file_path)

plane_names = {
    4201: 'TX83-NF',
    4202: 'TX83-NCF',
    4203: 'TX83-CF',
    4204: 'TX83-SCF',
    4205: 'TX83-SF'
}

# Actual .prj file contents for each plane name
prj_files = {
    'TX83-NF': "PROJCS[\"NAD_1983_StatePlane_Texas_North_FIPS_4201_Feet\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.000,298.25722210]],PRIMEM[\"Greenwich\",0],UNIT[\"Degree\",0.017453292519943295]],PROJECTION[\"Lambert_Conformal_Conic\"],PARAMETER[\"False_Easting\",656166.667],PARAMETER[\"False_Northing\",3280833.333],PARAMETER[\"Central_Meridian\",-101.50000000000000],PARAMETER[\"Latitude_Of_Origin\",34.00000000000000],PARAMETER[\"Standard_Parallel_1\",36.18333333333333],PARAMETER[\"Standard_Parallel_2\",34.65000000000000],UNIT[\"Foot_US\",0.30480060960122]]",
    'TX83-NCF': "PROJCS[\"NAD_1983_StatePlane_Texas_North_Central_FIPS_4202_Feet\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.000,298.25722210]],PRIMEM[\"Greenwich\",0],UNIT[\"Degree\",0.017453292519943295]],PROJECTION[\"Lambert_Conformal_Conic\"],PARAMETER[\"False_Easting\",1968500.000],PARAMETER[\"False_Northing\",6561666.667],PARAMETER[\"Central_Meridian\",-98.50000000000000],PARAMETER[\"Latitude_Of_Origin\",31.66666666666666],PARAMETER[\"Standard_Parallel_1\",33.96666666666667],PARAMETER[\"Standard_Parallel_2\",32.13333333333333],UNIT[\"Foot_US\",0.30480060960122]]",
    'TX83-CF': "PROJCS[\"NAD_1983_StatePlane_Texas_Central_FIPS_4203_Feet\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.000,298.25722210]],PRIMEM[\"Greenwich\",0],UNIT[\"Degree\",0.017453292519943295]],PROJECTION[\"Lambert_Conformal_Conic\"],PARAMETER[\"False_Easting\",2296583.333],PARAMETER[\"False_Northing\",9842500.000],PARAMETER[\"Central_Meridian\",-100.33333333333300],PARAMETER[\"Latitude_Of_Origin\",29.66666666666666],PARAMETER[\"Standard_Parallel_1\",31.88333333333333],PARAMETER[\"Standard_Parallel_2\",30.11666666666667],UNIT[\"Foot_US\",0.30480060960122]]",
    'TX83-SCF': "PROJCS[\"NAD_1983_StatePlane_Texas_South_Central_FIPS_4204_Feet\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.000,298.25722210]],PRIMEM[\"Greenwich\",0],UNIT[\"Degree\",0.017453292519943295]],PROJECTION[\"Lambert_Conformal_Conic\"],PARAMETER[\"False_Easting\",1968500.000],PARAMETER[\"False_Northing\",13123333.333],PARAMETER[\"Central_Meridian\",-99.00000000000000],PARAMETER[\"Latitude_Of_Origin\",27.83333333333333],PARAMETER[\"Standard_Parallel_1\",30.28333333333333],PARAMETER[\"Standard_Parallel_2\",28.38333333333333],UNIT[\"Foot_US\",0.30480060960122]]",
    'TX83-SF': "PROJCS[\"NAD_1983_StatePlane_Texas_South_FIPS_4205_Feet\",GEOGCS[\"GCS_North_American_1983\",DATUM[\"D_North_American_1983\",SPHEROID[\"GRS_1980\",6378137.000,298.25722210]],PRIMEM[\"Greenwich\",0],UNIT[\"Degree\",0.017453292519943295]],PROJECTION[\"Lambert_Conformal_Conic\"],PARAMETER[\"False_Easting\",984250.000],PARAMETER[\"False_Northing\",16404166.667],PARAMETER[\"Central_Meridian\",-98.50000000000000],PARAMETER[\"Latitude_Of_Origin\",25.66666666666666],PARAMETER[\"Standard_Parallel_1\",27.83333333333333],PARAMETER[\"Standard_Parallel_2\",26.16666666666666],UNIT[\"Foot_US\",0.30480060960122]]"
}

st.title("Texas SPCS83 Zones")

combined_options = pd.concat([df['zip'].astype(str), df['city'], df['county']]).unique()
search_input = st.selectbox("Select a zip code, city, or county:", combined_options)

if search_input:
    zip_result = df[df['zip'].astype(str) == search_input]
    city_result = df[df['city'].str.capitalize() == search_input.capitalize()]
    county_result = df[df['county'].str.capitalize() == search_input.capitalize()]

    result = pd.concat([zip_result, city_result, county_result]).drop_duplicates(subset=['SPCS83_Code'])

    if not result.empty:
        for _, row in result.iterrows():
            spcs83_code = row['SPCS83_Code']
            plane_name = plane_names.get(spcs83_code, "Unknown")
            
            if row['city'].capitalize() == search_input.capitalize():
                result_type = "city"
            elif row['county'].capitalize() == search_input.capitalize():
                result_type = "county"
            else:
                result_type = "zip code"
            
            st.write(f"The plane name for {search_input} ({result_type}) is {plane_name}")

            st.code(plane_name, language="text")
            st.markdown("Click the button above to copy the plane name.")
            
            # Add download button for the .prj file
            prj_content = prj_files.get(plane_name, "No .prj file available.")
            st.download_button(
                label=f"Download {plane_name}.prj",
                data=prj_content,
                file_name=f"{plane_name}.prj",
                mime="text/plain"
            )
            st.markdown("---")
    else:
        st.write(f"No data found for {search_input}")
