import streamlit as st
import pandas as pd 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

#@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.DataFrame({'fruit':['Apple', 'Banana'], 'unit_price':[50,25], 'num_units':[0,0], 'total_price':[0,0]})
    return df

loaded_data = load_data()

num_units = st.slider('Select Number of Units', 0, 130, 1)
loaded_data['num_units'] = num_units

js_calculate_total = JsCode("""

    function (params) {
        
         var unit_price = params.data.unit_price;
         var num_units = params.data.num_units;
         return (unit_price * num_units).toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0});

    }

""")

gb = GridOptionsBuilder.from_dataframe(loaded_data) #Infer basic colDefs from dataframe types
# Grid Builder configurations
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
# Below, the first parameters are all the same as in the load_data dateframe, but the "header_name" is what is displayed and can be anything 
gb.configure_column("fruit", header_name='Fruit', pivot=True, sort='asc')
gb.configure_column("unit_price", header_name='Unit Price', sort='desc', type=["numericColumn","numberColumnFilter"], valueFormatter="data.estimatednotional_usd.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0})", aggFunc='sum') # defines numeric column
gb.configure_column("total_price", header_name='Total Price', type=["numericColumn","numberColumnFilter"], editable=False, valueGetter=js_calculate_total) # uses custom value getter for calculated column
gridOptions = gb.build()
                            
grid_response = AgGrid(
        loaded_data,
        gridOptions = gridOptions,
        height=200,
        width='100%', # how much of the Streamlit page width this grid takes up
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True, # automatically fits all columns to be displayed in the grid in one view (doesn't always seem to work)
        allow_unsafe_jscode=True, # Set to True to allow the Javascript code to be injected
        enable_enterprise_modules=True, # enables right click and fancy features - can add license key as another parameter (license_key='string') if you have one
        key='select_grid', # stops grid from re-initialising every time the script is run
        reload_data=True # allows modifications to loaded_data to update this same grid entity
        #theme='light'
        )

st.write(grid_response['data'])
st.write(gridOptions.get('columnDefs'))
st.write(gridOptions.get('defaultColDef'))