import streamlit as st
# from functions import this_is_it
import pandas as pd
import pyodbc
import plotly.express as px

header = st.container()
dataset = st.container()

with header:
    st.title("Welcome to my first web-app try")



result = st.button("Let's run the script! You will need to wait up to 1 Minute until you can download the file")

st.write(result)

if result:
    # from datetime import datetime  # für Zeitüberwachung des SQL-Querys

    # import pandas as pd
    # import plotly.express as px
    # import pyodbc  # odbc-connection (für DB)


    # HDBODBC angeben (Name des SAP-ODBC)
    db_conn = pyodbc.connect(DSN='SAP-HANA-P30')

    # Tipp: Zu finden unter: Windows-Taste -> App "ODBC-Datenquellen (64-Bit)" -> Reiter "System-DSN" -> Name der DB auswählen

    # SQL-Query definieren (kann 1:1 aus dem SAP HANA Studio kopiert werden - vorangehend 3x Symbol ", ebenso am Ende)
    sql_query = """SELECT
        A2."SCORE_CLASS",
        A1."SORTIMENTS_GRUPPE",
        A1."ALTER_HEUTE",
        MIN(A1."EGT"),
        A1."ALTERSSEGMENT",
        A2."MODEL_RUN_DATE"
            
    FROM "_SYS_BIC"."sbb.app.ucv/KUNDE_ABO_LEISTUNG"('PLACEHOLDER' = ('$$MIN_LAUFZEIT_VZ$$', '7')) AS A1

    LEFT OUTER JOIN "_SYS_BIC"."sbb.app.ucv.btl.kwert/SCORE_ML" AS A2
    ON A1."KUNDE" = A2."CKM"

    WHERE A1."SORTIMENTS_GRUPPE" = 'GA' AND ("STATUS_KARTE" <= '09' or "STATUS_KARTE" is NULL) AND
        "MODEL_ID" = 'NDV_202104_01_A' AND "MODEL_RUN_DATE">='2022-01-01' AND "MODEL_RUN_DATE" <= '2022-06-30' AND "ALTERSSEGMENT" = 'Seniors'
        AND "EGT">='2022-01-01' AND "EGT" <= '2022-09-30'
        
    GROUP BY 	
        A2."SCORE_CLASS",
        A1."SORTIMENTS_GRUPPE",
        A1."ALTER_HEUTE",
        A1."ALTERSSEGMENT",
        A2."MODEL_RUN_DATE"
        
        

    """

    # SQL-Query ausführen mit Zeitüberwachung

    # Starzeit auslesen
    start = datetime.now()

    # Ausführen der SQL-Query
    newdf = pd.read_sql_query(sql_query, db_conn
                        #,dtype={'PREIS': np.float32, 'IS_B2B': np.float32} # hier können Datatypes bereits mitgegeben werden
                        ) 

    # Endzeit auslesen
    ende = datetime.now()

    # Dauer der SQL-Query ausgeben
    print("Dauer SQL-Query:", ende-start)

    newdf["Counter"] = 1
    newdf.rename(columns = {'MIN(EGT)':'EGT'}, inplace = True)
    # newdf.to_csv(r"C:\Users\u238133\OneDrive - SBB\Dokumente\Coding Area\Tasks\Rüdiger Abfrage Score ML\data.csv")











result_2 = st.button("Earn your download!")

st.write(result_2)

if result_2:

    st.write(":smile:")
    # this_is_it()

    @st.cache
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    # csv = convert_df("C:\Users\u238133\OneDrive - SBB\Dokumente\Coding Area\DokumentDownloader\test_data.csv")
    # csv = pd.read_csv(r"C:\Users\u238133\OneDrive - SBB\Dokumente\Coding Area\DokumentDownloader\test_data.csv")
csv = 
    csv = convert_df(csv)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
)
