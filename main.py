import geopandas as gpd
import pandas as pd
from shapely.geometry import *

def transforme_point (x) :
    abs = float(x.split(',')[0])
    ord = float(x.split(',')[1])
    return (Point([abs,ord]))

def transforme_polygone (x) :
    lecture = x.split('[')
    type_shape = lecture[0].split("\"")[3]
    coord = []
    if type_shape == "Polygon" :
        for i in range(4,len(lecture)) :
            try :
                abs = float(lecture[i].split(',')[0])
                ord = float(lecture[i].split(',')[1].split(']')[0])
                coord += [[abs, ord]]
            except ValueError :
                type_shape = 'MultiPolygon'
        return (Polygon(coord))
    if type_shape == 'MultiPolygon':
        lecture = x.split('[[')
        multi_poly = []
        coord = []
        abs = float(lecture[2].split(']')[0].split('[')[0].split(',')[0])
        ord = float(lecture[2].split(']')[0].split('[')[0].split(',')[1])
        coord += [[abs, ord]]
        for i in range(1,len(lecture[2].split(']')) - 3) :
            abs = float(lecture[2].split(']')[i].split('[')[1].split(',')[0])
            ord = float(lecture[2].split(']')[i].split('[')[1].split(',')[1])
            coord += [[abs, ord]]
        multi_poly += [Polygon(coord)]
        for pol in range(3, len(lecture)) :
            coord = []
            abs = float(lecture[pol].split(']')[0].split(',')[0].replace("[",""))
            ord = float(lecture[pol].split(']')[0].split(',')[1])
            coord += [(abs, ord)]
            for i in range(1, len(lecture[pol].split(']')) - 4):
                abs = float(lecture[pol].split(']')[i].split('[')[1].split(',')[0])
                ord = float(lecture[pol].split(']')[i].split('[')[1].split(',')[1])
                coord += [(abs, ord)]
        multi_poly+= [Polygon(coord)]
        return (MultiPolygon(multi_poly))


def compte_poste(point,  geo_shape) :
    if point.within(geo_shape) :
        return(1)
    else :
        return (0)

def nombre_poste(x,borne_gdf) :
    return (borne_gdf.loc[borne_gdf["Geo Point"] == x].shape[0])

def find_match_poste(geo_point, IRIS_gdf) :
    for ind_iris in IRIS_gdf :


def main(path_to_csv_borne, path_to_csv_IRIS) :
    print("Lecture du fichier ENEDIS")
    borne_gdf = pd.read_csv (path_to_csv_borne, sep = ';')
    borne_gdf["Geo Point"] = borne_gdf["Geo Point"].apply(lambda  x : transforme_point(x))
    print("Lecture du fichier IRIS")
    IRIS_gdf  = pd.read_csv (path_to_csv_IRIS, sep = ';')
    IRIS_gdf["geo_shape"]  = IRIS_gdf["geo_shape"].apply(lambda  x : transforme_polygone(x))
    print("Création du DataFrame de sortie")
    res_df = IRIS_gdf[["Code de la maille IRIS","nom_reg","geo_shape"]].copy()
    res_df.columns = ["Code de la maille IRIS","Nombre de postes électriques","geo_shape"]
    res_df["Nombre de postes électriques"] = 0
    print("Calcul du nombre de bornes dans chaque IRIS")
    # for ind in res_df.index :
    #     res_df.at[ind,"Nombre de postes électriques"] = borne_gdf["Geo Point"].apply(lambda x : compte_poste(x, res_df.at[ind,"Nombre de postes électriques"],res_df.at[ind,"geo_shape"]) )
    borne_gdf["Geo Point"] = borne_gdf["Geo Point"].apply(lambda x : find_match_poste(x, IRIS_gdf))
    res_df["Nombre de postes électriques"] = res_df["Code de la maille IRIS"]
    res_df["Nombre de postes électriques"] = res_df["Nombre de postes électriques"].apply(lambda x : nombre_poste(x,borne_gdf))
    # for ind_IRIS in res_df.index :
    #     for ind_borne in borne_gdf.index :
    #         res_df.at[ind_IRIS, "Nombre de postes électriques"] += compte_poste(borne_gdf.at[ind_borne, "Geo Point"], res_df.at[ind_IRIS, "geo_shape"])
    print("Ecriture dans le fichier de sortie")
    res_df.to_excel("C:/Users/ldemontella/Documents/Repartition_Infrastructure_IRIS/sortie.xlsx")



path_to_csv_borne = "C:/Users/ldemontella/Documents/Repartition_Infrastructure_IRIS/poste-electrique.csv"
path_to_csv_IRIS = "C:/Users/ldemontella/Documents/Repartition_Infrastructure_IRIS/contours-iris.csv"

main(path_to_csv_borne, path_to_csv_IRIS)