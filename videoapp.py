import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
#import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
#Deprecaction -- To update with newest method
st.set_option('deprecation.showPyplotGlobalUse', False)
#General Analysis
st.title("Video Game EDA")
activity = ["Basico EDA", "Multiplataforma","Geografía","Género","ESRB","Acuerdo"]
choice = st.sidebar.selectbox("Main activity",activity)
st.markdown("[Fuente: Kaggle video game sales](https://www.kaggle.com/ashaheedq/video-games-sales-2019)")
#Dataset Kaggle
df0 = pd.read_csv("vgsales-12-4-2019.csv")

#Analysis starts here
def main():
    if choice == "Basico EDA":
        st.title('Análisis básico')
        st.text("¿Tamaño del dataset?")
        st.write(df0.shape)
        st.text("5 primeras filas:")
        st.write(df0.head(5))
        st.text("Descripción general:")
        st.write(df0.describe(include='all'))
        st.text("¿Qué tipo de datos tengo?")
        st.write(df0.dtypes)
        st.text("¿Datos nulos?:")
        st.write(df0.isnull().sum())
        st.text("Análisis de correlación tipo de datos numéricos:")
        f, az = plt.subplots(figsize=(12, 9))
        st.write(sns.heatmap(df0.corr(), vmax=.8, square=True, annot=True))
        st.pyplot()

    elif choice == "Multiplataforma":
        st.subheader('Análisis videojuegos multiplataforma')
        if st.checkbox('¿Debo desarrollar juegos multiplataforma?¿O enfocarme sólo en una plataforma'):
            st.text('Sí, debería desarrollar juegos para dos plataformas específicas')
        if st.checkbox('¿En qué plataforma me debería enfocar?'):
        #Data clean
            dfpivot = pd.pivot_table(df0, values='Global_Sales', index=['Year'], columns='Platform')
            dfpivot['Globalsales'] = dfpivot.iloc[:].sum(axis=1)
            dfpivot5 = dfpivot.iloc[-2:]
            dfpivot5 = dfpivot5.dropna(axis=1, how='all')
            fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
            platforms = list(dfpivot5.columns)
            gsales = list(dfpivot5.Globalsales)

            #Gráfico - Multiplataforma
            def func(pct, allvals):
                absolute = int(pct / 100. * np.sum(allvals))
                return "{:.1f}%\n".format(pct, absolute)

            wedges, texts, autotexts = ax.pie(gsales, autopct=lambda pct: func(pct, gsales),
                                              textprops=dict(color="w"))

            ax.legend(wedges, platforms,
                      title="Platforms",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1))

            plt.setp(autotexts, size=8, weight="bold")

            ax.set_title("Multiplataforma según ventas globales últimos en los últimos 2 años")
            st.pyplot()

    elif choice == "Geografía":
        st.subheader('Análisis ventas según geografía')
        if st.checkbox('¿Puedo esperar que mis ventas se repartan por igual entre las distintas geografías?'):
            st.text("No hay un reparto equitativo. Disponemos de pocos datos para constatar esta distibución")
            st.markdown(
                "[Top ventas USA 2020](https://www.google.com/search?safe=active&rlz=1C1CHBF_esES906ES906&sxsrf=ALeKk00B8icxo_rRoNP-XHR0uAD3vKSEYg%3A1605980379686&ei=21C5X5qNKYykUs33u-gF&q=top+ventas+videojuegos+usa+2020&oq=top+ventas+videojuegos+usa+2020&gs_lcp=CgZwc3ktYWIQAzoECAAQRzoECCMQJzoICCEQFhAdEB5QvMgBWKjvAWC49AFoAXACeAGAAacDiAHHG5IBCTAuMS4wLjcuMpgBAKABAqABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwja5q-Ql5TtAhUMkhQKHc37Dl0Q4dUDCA0&uact=5)")

            if st.checkbox('Ventas USA'):
                # Data clean
                dfpivot = pd.pivot_table(df0, values='NA_Sales', index=['Year'], columns='Name')
                dfpivot['NA_Sales'] = dfpivot.iloc[:].sum(axis=1)
                dfpivot5 = dfpivot.iloc[-2:]
                dfpivot5 = dfpivot5.dropna(axis=1, how='all')
                fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
                vname = list(dfpivot5.columns)
                usasales = list(dfpivot5.NA_Sales)

                # Gráfico - Multiplataforma
                def func(pct, allvals):
                    absolute = int(pct / 100. * np.sum(allvals))
                    return "{:.1f}%\n".format(pct, absolute)

                wedges, texts, autotexts = ax.pie(usasales, autopct=lambda pct: func(pct, usasales),
                                                  textprops=dict(color="w"))

                ax.legend(wedges, vname,
                          title="Name",
                          loc="center left",
                          bbox_to_anchor=(1, 0, 0.5, 1))

                plt.setp(autotexts, size=8, weight="bold")

                ax.set_title("% de videojuegos vendidos en Norte América en los últimos 2 años")
                st.pyplot()

            st.markdown(
                "[Top ventas Japón 2020](https://www.google.com/search?safe=active&rlz=1C1CHBF_esES906ES906&sxsrf=ALeKk01HM43ScXp4P3FXTZcuJQRJcJ2DJA%3A1606043784316&ei=iEi6X6PgEtSejLsPpdOI-AY&q=top+ventas+videojuegos+jap%C3%B3n+2020&oq=top+ventas+videojuegos+jap%C3%B3n+2020&gs_lcp=CgZwc3ktYWIQAzoECAAQR1DJjQFY_aYBYPKoAWgBcAJ4AIAB8AOIAbkmkgEFMy03LjWYAQCgAQGqAQdnd3Mtd2l6yAEDwAEB&sclient=psy-ab&ved=0ahUKEwijxIeqg5btAhVUD2MBHaUpAm8Q4dUDCA0&uact=5)")
            if st.checkbox('Ventas JP'):
                # Data clean
                dfpivot = pd.pivot_table(df0, values='JP_Sales', index=['Year'], columns='Name')
                dfpivot['JP_Sales'] = dfpivot.iloc[:].sum(axis=1)
                dfpivot5 = dfpivot.iloc[-2:]
                dfpivot5 = dfpivot5.dropna(axis=1, how='all')
                fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
                vname = list(dfpivot5.columns)
                jpsales = list(dfpivot5.JP_Sales)

                # Gráfico - Multiplataforma
                def func(pct, allvals):
                    absolute = int(pct / 100. * np.sum(allvals))
                    return "{:.1f}%\n".format(pct, absolute)

                wedges, texts, autotexts = ax.pie(jpsales, autopct=lambda pct: func(pct, jpsales),
                                                  textprops=dict(color="w"))

                ax.legend(wedges, vname,
                          title="Name",
                          loc="center left",
                          bbox_to_anchor=(1, 0, 0.5, 1))

                plt.setp(autotexts, size=8, weight="bold")

                ax.set_title("% de videojuegos vendidos en Japón en los últimos 2 años")
                st.pyplot()

            st.markdown(
                "[Top ventas Europa 2020](https://www.google.com/search?safe=active&rlz=1C1CHBF_esES906ES906&sxsrf=ALeKk03UkTOibcQWE9wBIl2olBY1WnqFYQ:1606043830006&q=top+ventas+videojuegos+europa+2020&spell=1&sa=X&ved=2ahUKEwj8r-y_g5btAhXh0eAKHSpAAkEQBSgAegQIChA1&biw=872&bih=865)")
            if st.checkbox('Ventas Europa'):
                # Data clean
                dfpivot = pd.pivot_table(df0, values='PAL_Sales', index=['Year'], columns='Name')
                dfpivot['PAL_Sales'] = dfpivot.iloc[:].sum(axis=1)
                dfpivot5 = dfpivot.iloc[-3:]
                dfpivot5 = dfpivot5.dropna(axis=1, how='all')
                fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
                vname = list(dfpivot5.columns)
                palsales = list(dfpivot5.PAL_Sales)

                # Gráfico - Multiplataforma
                def func(pct, allvals):
                    absolute = int(pct / 100. * np.sum(allvals))
                    return "{:.1f}%\n".format(pct, absolute)

                wedges, texts, autotexts = ax.pie(palsales, autopct=lambda pct: func(pct, palsales),
                                                  textprops=dict(color="w"))

                ax.legend(wedges, vname,
                          title="Name",
                          loc="center left",
                          bbox_to_anchor=(1, 0, 0.5, 1))

                plt.setp(autotexts, size=8, weight="bold")

                ax.set_title("% de videojuegos vendidos en Europa en los últimos 3 años")
                st.pyplot()
    elif choice == "Género":
        st.subheader('Análisis género del videojuego')
        if st.checkbox('¿Qué géneros tendría que desarrollar?'):
            df3 = df0[['Year', 'Genre', 'Global_Sales', 'Rank', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']]
            df3pivot = pd.pivot_table(df3, index=["Year", "Genre"],
                                      values=["Global_Sales", "NA_Sales", "PAL_Sales", "JP_Sales", "Other_Sales"],
                                      aggfunc=[np.sum])
            st.write(df3pivot.tail(33))

        if st.checkbox('¿Existe algún género que me garantice ventas en todos los mercados?'):
            st.text("Acción, Juegos de rol y deportes")
            df4 = df0[['Year', 'Genre', 'Global_Sales','NA_Sales', 'PAL_Sales', 'JP_Sales']]
            subset_data = df4
            genre_input = st.sidebar.multiselect('Genre',
                                                 df4.groupby('Genre').count().reset_index()['Genre'].tolist())
            if len(genre_input) > 0:
                subset_data = df4[df4['Genre'].isin(genre_input)]
            st.subheader('Género según ventas globales')
            totalcases = alt.Chart(subset_data).transform_filter(alt.datum.Global_Sales > 0).mark_line().encode(
                x=alt.X('Year', type='nominal', title='Year'),
                y=alt.Y('sum(Global_Sales):Q', title='Global Sales'),
                color='Genre',
                tooltip = 'sum(Global_Sales)',
            ).properties(
                width=1500,
                height=600
            ).configure_axis(
                labelFontSize=17,
                titleFontSize=20
            )
            st.altair_chart(totalcases)

    elif choice == "ESRB":
        st.subheader('Análisis ESRB')
        df5 = df0[['Year','Name','ESRB_Rating','Rank','Global_Sales']]

        if st.checkbox('¿Consiguen menos ventas los videojuegos clasificados sólo para mayores (ESRB Rating)?¿O ocurre lo contrario?'):
            st.text("No, ocurre lo contrario")
            subset_data = df5
            esrb_input = st.sidebar.multiselect('ESRB_Rating',
                                                 df5.groupby('ESRB_Rating').count().reset_index()['ESRB_Rating'].tolist())
            if len(esrb_input) > 0:
                subset_data = df5[df5['ESRB_Rating'].isin(esrb_input)]
            st.subheader('ESRB rating por ventas globales')
            totalcases = alt.Chart(subset_data).transform_filter(alt.datum.Global_Sales > 0).mark_line().encode(
                x=alt.X('Year', type='nominal', title='Year'),
                y=alt.Y('sum(Global_Sales):Q', title='Global Sales'),
                color='ESRB_Rating',
                tooltip='sum(Global_Sales)',
            ).properties(
                width=1500,
                height=600
            ).configure_axis(
                labelFontSize=17,
                titleFontSize=20
            )
            st.altair_chart(totalcases)

    elif choice == "Acuerdo":
        if st.checkbox('¿Sería beneficioso conseguir un acuerdo de distribución con alguna distribuidora?'):
        #Data clean
            dfpivot = pd.pivot_table(df0, values='Global_Sales', index=['Year'], columns='Publisher')
            dfpivot['Globalsales'] = dfpivot.iloc[:].sum(axis=1)
            dfpivot5 = dfpivot.iloc[-3:]
            dfpivot5 = dfpivot5.dropna(axis=1, how='all')
            fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
            publisher = list(dfpivot5.columns)
            gsales = list(dfpivot5.Globalsales)

            #Gráfico - Multiplataforma
            def func(pct, allvals):
                absolute = int(pct / 100. * np.sum(allvals))
                return "{:.1f}%\n".format(pct, absolute)

            wedges, texts, autotexts = ax.pie(gsales, autopct=lambda pct: func(pct, gsales),
                                              textprops=dict(color="w"))

            ax.legend(wedges, publisher,
                      title="Publisher",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1))

            plt.setp(autotexts, size=8, weight="bold")

            ax.set_title("Ventas globales según distribuidor en los últimos 3 años")
            st.pyplot()

        dfpivot = pd.pivot_table(df0, values='Global_Sales', index=['Year'], columns='Publisher')
        dfpivot['Globalsales'] = dfpivot.iloc[:].sum(axis=1)
        dfpivot5 = dfpivot.iloc[-2:]
        dfpivot5 = dfpivot5.dropna(axis=1, how='all')
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        publisher = list(dfpivot5.columns)
        gsales = list(dfpivot5.Globalsales)

        # Gráfico - Multiplataforma
        def func(pct, allvals):
            absolute = int(pct / 100. * np.sum(allvals))
            return "{:.1f}%\n".format(pct, absolute)

        wedges, texts, autotexts = ax.pie(gsales, autopct=lambda pct: func(pct, gsales),
                                          textprops=dict(color="w"))

        ax.legend(wedges, publisher,
                  title="Publisher",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title("Ventas globales según distribuidor en los últimos 2 años")
        st.pyplot()

        df5 = df0[['Year', 'Name', 'Publisher', 'Rank', 'Global_Sales']]
        if st.checkbox(
                '¿Todas dan el mismo servicio?'):
            subset_data = df5
            esrb_input = st.sidebar.multiselect('Publisher',
                                                df5.groupby('Publisher').count().reset_index()[
                                                    'Publisher'].tolist())
            if len(esrb_input) > 0:
                subset_data = df5[df5['Publisher'].isin(esrb_input)]
            st.subheader('Distribuidora según ventas globales')
            totalcases = alt.Chart(subset_data).transform_filter(alt.datum.Global_Sales > 0).mark_line().encode(
                x=alt.X('Year', type='nominal', title='Year'),
                y=alt.Y('sum(Global_Sales):Q', title='Global Sales'),
                color='Publisher',
                tooltip='sum(Global_Sales)',
            ).properties(
                width=1500,
                height=600
            ).configure_axis(
                labelFontSize=17,
                titleFontSize=20
            )
            st.altair_chart(totalcases)

if __name__ == '__main__':
    main()
