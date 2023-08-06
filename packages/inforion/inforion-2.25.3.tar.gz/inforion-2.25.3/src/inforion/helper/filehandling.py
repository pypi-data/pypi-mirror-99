import os
import sys
import pandas as pd




def checkfile_exists(file):
    if os.path.exists(file) is False:
        return False
    else:
        return True


def checkfiletype(filepath):

    # Split the extension from the path and normalise it to lowercase.
    ext = os.path.splitext(filepath)[-1].lower()

    if ext == ".csv" or ext == ".xlsx" or ext == ".xls":
        return ext
    else:
        print("Type is not supported")
        sys.exit(0)


def loadfile(file):

    ext = checkfiletype(file)

    if ext == ".csv":
        df = pd.read_csv(file)
    elif ext == ".xlsx" or ext == ".xls":
        df = pd.read_excel(file)
    return df


def savetodisk(file, df):

    ext = checkfiletype(file)

    if ext == ".csv":
        df.to_csv(file)
    else:

        writer = pd.ExcelWriter(file, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Log Output", index=False)
        writer.save()


def getDataFrame(inputfile):
    checkfiletype(inputfile)
    df = loadfile(inputfile)
    return df


def mergedata(sheet1, sheet2, column, mtype):
    merged = sheet1.merge(sheet2, on=column, how=mtype)
    return merged
