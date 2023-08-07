# General
import datetime
import os
import pickle
import warnings
import argparse
import logging
import json
from datetime import date
from math import log
# Data
import pandas as pd
import numpy as np
import regex as re
# ML
# Used in : Data_Engineering
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer  # Used in : Data_Engineering
from sklearn.linear_model import BayesianRidge  # Used in : Data_Engineering
from sklearn.exceptions import DataConversionWarning


logger = logging.getLogger(__name__)




def set_dataframe_columntypes(df):
    """Manual setting of the datatypes

    Args:
        df ([dataframe]): [dataframe with the leads information]

    Returns:
       df [df]: [Dataframe with the leads information, with the new types]
    """
    logger.info("Changing data types")
    df = clean_rows_with_na( df=df, cols_to_clean_na=['IDEmailStatus'] )
    if 'idLead' in df:
        df['idLead'] = df['idLead'].astype('int32')
    if 'idCampaign' in df:
        df['idCampaign'] = df['idCampaign'].astype('int8')
    if 'campaign_bulk_date' in df:
        df['campaign_bulk_date'] = df['campaign_bulk_date'].astype('object')
        df['campaign_bulk_date'] = pd.to_datetime(df['campaign_bulk_date'])
        df['campaign_bulk_date'] = df['campaign_bulk_date'].dt.date
    if 'IDEmailStatus' in df:
        df['IDEmailStatus'] = df['IDEmailStatus'].astype('int8')
    if 'Ranking' in df:
        df['Ranking'] = df['Ranking'].astype('float32')
    if 'BV' in df:
        df['BV'] = df['BV'].astype('float32')
    if 'Size' in df:
        df['Size'] = df['Size'].astype('object')
    if 'Industry' in df:
        df['Industry'] = df['Industry'].astype('object')
    if 'CompanyFollowers' in df:
        df['CompanyFollowers'] = df['CompanyFollowers'].astype('object')
    if 'QEmployeesOnLinkedIn' in df:
        df['QEmployeesOnLinkedIn'] = df['QEmployeesOnLinkedIn'].astype('float64')
    if 'Type' in df:
        df['Type'] = df['Type'].astype('object')
    if 'Specialties' in df:
        df['Specialties'] = df['Specialties'].astype('object')
    if 'MXType' in df:
        df['MXType'] = df['MXType'].astype('object')
    if 'Technologies' in df:
        df['Technologies'] = df['Technologies'].astype('object')
    if 'Country' in df:
        df['Country'] = df['Country'].astype('object')
    if 'State' in df:
        df['State'] = df['State'].astype('object')
    if 'Title' in df:
        df['Title'] = df['Title'].astype('object')
    if 'kw_key' in df:
        df['kw_key'] = df['kw_key'].astype('object')
    if 'Seniority' in df:
        df['Seniority'] = df['Seniority'].astype('object')
    if 'Department' in df:
        df['Department'] = df['Department'].astype('object')
    if 'LeadConnections' in df:
        df['LeadConnections'] = df['LeadConnections'].astype('float64')
    if 'LeadFollowers' in df:
        df['LeadFollowers'] = df['LeadFollowers'].astype('float64')
    if 'PreviousContacts' in df:
        df['PreviousContacts'] = df['PreviousContacts'].astype('float16')
    if 'PreviousStatus' in df:
        df['PreviousStatus'] = df['PreviousStatus'].astype('float16')
    if 'DaysSinceLastContact' in df:
        df['DaysSinceLastContact'] = df['DaysSinceLastContact'].astype(
            'float16')
    if 'DaysSinceFirstContact' in df:
        df['DaysSinceFirstContact'] = df['DaysSinceFirstContact'].astype(
            'float16')
    if 'DaysSincePositionStart' in df:
        df['DaysSincePositionStart'] = df['DaysSincePositionStart'].astype(
            'float16')
    return df


def clean_previous_status(df, status_to_clean):
    """Eliminate rows with a defined previous status value
    Args:
        df ([dataframe]): [dataframe with the leads]
        status_to_clean ([list of ints]): [list with the status to clean]

    Returns:
        df [dataframe]: [dataframe with the leads]
    """

    logger.info(f"Cleaning invalid previous status ( {status_to_clean})")
    for status in status_to_clean:
        if 'PreviousStatus' in df:
            df = df[df.PreviousStatus != status]
    return df


def clean_rows_with_na(df,cols_to_clean_na):
    """Eliminates rows with NAs in Attributes with low % NA Percentage

    Args:
        df ([dataframe]): Leads dataframe
    Returns:
        df [dataframe]: [dataframe with the leads]
    """
    # logger  amount of rows
    nrows_pre = df.shape[0]
    logger.info( f"Original rows: {nrows_pre}" )

    for col in cols_to_clean_na:
        if col in df:
            nas_sum = df[col].isna().sum()
            logger.info(f"NAs in {col}: {nas_sum}")
            df = df[df[col].notna()]
    nrows_post = df.shape[0]
    percentage_eliminated = (nrows_pre - nrows_post) / nrows_pre * 100
    logger.info( f" Rows after deleting rows with NA: {nrows_post}, Percentage: {percentage_eliminated}" )

    return df


def fill_na_with_unknown(df, columns):
    """[summary]
    Args:
        df ([dataframe]): [dataframe with the leads]
        columns ([list of strings]): [list with the names of the columns]
    Returns:
        df [dataframe]: [dataframe with the leads]
    """
    for col in columns:
        if col in df.columns:
            logger.info(f'filling NA in {col} with "unknown" ')
            df[col] = df[col].fillna('Unknown')
    return df


def create_specialties_flag(df):
    """Converts specialties to a flag that determines if the company has them

    Args:
        df ([dataframe]): Dataframe with leads
    Returns:
        df ([dataframe]): Dataframe with leads
    """
    logger.info("Creating Specialties flag")
    df['Has Specialties'] = df['Specialties'].isna()
    df['Has Specialties'] *= 1
    df['Has Specialties'] = df['Has Specialties'].astype("category")
    return df


def set_idemailstatus_target_column(df):

    if ('IDEmailStatus' in df.columns):
        logger.info('Setting E-Mail status target ')
        df = df[~df['IDEmailStatus'].isin([3, 5, 7, 32])]
        df.loc[df['IDEmailStatus'] != 14, 'IDEmailStatus'] = 0
        df.loc[df['IDEmailStatus'] == 14, 'IDEmailStatus'] = 1
    else:
        logger.error('No IDEmailSTatus column found')
        raise Exception('No IDEmailStatus column found!!!!!')
    return df


def set_bv_target_column(df):
    if('BV' in df.columns):
        logger.info('Setting BV status target ')
        df = df[df.BV.notna()]
        df['BV']=df['BV'].astype('float32')
    else:
        logger.error('No BV column found')
        raise Exception('No BV column found!!!!!')
    #   df = df[df.BV < 40]
    return df


def set_bv_discrete_target_column(df,bins):
    if('BV' in df.columns):
        logger.info('Setting BV status target for classification ')
        df.BV.fillna(value=0,inplace=True)
        labels = [0, 1, 2, 3, 4, 5]
        df.insert(loc=1,column='BV_cut', value= pd.cut(x=df['BV'], bins = bins,labels=labels).astype('float32'))
    else:
        logger.error('No BV column found')
        raise Exception('No BV column found!!!!!')
    return df

def set_target_column(df,model_type,bins):
    if model_type == 'probability':
        df = set_idemailstatus_target_column( df=df )
    elif model_type == 'bv':
        df = set_bv_target_column( df=df )
    elif model_type == 'multiclass':
        df = set_bv_discrete_target_column( df=df,bins=bins )
    else:
        raise Exception( 'Incorrect model_type !!!!!' )
    return df

def create_company_years_column(df):
    """Year founded, creation of the Company years category using Year founded

    Args:
        df ([dataframe]): [dataframe with the leads]

    Returns:
        df [dataframe]: [dataframe with the leads]
    """

    logger.info("Creating company years category")
    # Create Company years category
    if df['YearFounded'].dtype == object:
        df['YearFounded'] = df['YearFounded'].str.extract(
            '(\d{4})$', expand=False).astype('Float16')

    CurrentYear = date.today().year
    df['YearFounded'] = df['YearFounded'].fillna(0)
    df.loc[(CurrentYear - df['YearFounded'] <= 2),
           'CompanyYears'] = "0-2 Years"
    df.loc[(CurrentYear - df['YearFounded'] > 2) & (
        CurrentYear - df['YearFounded'] <= 5), 'CompanyYears'] = "0-2 Years"
    df.loc[(CurrentYear - df['YearFounded'] > 2) & (
        CurrentYear - df['YearFounded'] <= 5), 'CompanyYears'] = "3-5 Years"
    df.loc[(CurrentYear - df['YearFounded'] > 5) & (
        CurrentYear - df['YearFounded'] <= 10), 'CompanyYears'] = "6-10 Years"
    df.loc[(CurrentYear - df['YearFounded'] > 10) & (
        CurrentYear - df['YearFounded'] <= 25), 'CompanyYears'] = "11-25 Years"
    df.loc[(CurrentYear - df['YearFounded'] > 25) & (
        CurrentYear - df['YearFounded'] <= 50), 'CompanyYears'] = "26-50 Years"
    df.loc[(CurrentYear - df['YearFounded'] > 50),
           'CompanyYears'] = "51+ Years"
    # Errors go to "unknown category"
    df.loc[(df['YearFounded'] > CurrentYear) | (
        df['YearFounded'] < 1600), 'CompanyYears'] = "Unknown"
    df = df.drop(['YearFounded'], axis=1)
    return df


def fill_seniority_column(df):
    """Defines new cases for Seniority and sets the rest to 'other'

    Args:
        df ([dataframe]): [Dataframe with the leads]
    Returns:
        df [datafrane]: [dataframe with the leads]
    """
    logger.info("Filling Seniority from some Titles")
    df.loc[(df['Title'].str.contains('Specialist', 'Title')) &
           (df['Seniority'].isna()), 'Seniority'] = 'Specialist'
    df.loc[(df['Title'].str.contains('Associate', 'Title')) &
           (df['Seniority'].isna()), 'Seniority'] = 'Associate'
    df['Seniority'] = df['Seniority'].fillna('other')

    return df


def filter_countries(df, countries):
    logger.info(f'Filtering the following countries: {countries}')
    df = df[df['Country'].isin(countries)]
    return df


def convert_kwkey_specialties_and_technologies_to_int(df):
    """Using regular expressions, converts a comma separated list of keys and technologies into the number of elements of this columns

    Args:
        df ([dataframe]): [Dataframe with the leads]

    Returns:
       df [dataframe]: [Dataframe with the leads]
    """
    logger.info(f'Counting KeyWords')
    # number of elements in kw_key
    df['Nkw_key'] = df.kw_key.apply(
        lambda x: 0 if pd.isnull(x) else len(re.findall("(?:\".*?\"|\S)+", x)))
    # Number of elements in technologies
    logger.info( f'Counting Technologies' )
    df['NTechnologies'] = df.Technologies.apply(
        lambda x: 0 if pd.isnull(x) else len(re.split(',', x)))
    logger.info( f'Counting Specialties' )
    df['NSpecialties'] = df.Technologies.apply(
        lambda x: 0 if pd.isnull(x) else len(re.split(',', x)))

    return df


def fill_historic_variables(df):
    """SQL window functions returns NULLS when there is no data, we reset this to 0
    Args:
        df ([dataframe]): [Dataframe with the leads]

    Returns:
        df [dataframe]: [Dataframe with the leads]
    """
    logger.info(
        "Filling historic variables ( PContacts, PStatus,Daysince last and first contact)")
    if 'PreviousContacts' in df:
        df['PreviousContacts'] = df['PreviousContacts'].fillna(0)
    if 'PreviousStatus' in df:
        df['PreviousStatus'] = df['PreviousStatus'].fillna(0)
        df['PreviousStatus'] = df['PreviousStatus'].astype("category")
    if 'DaysSinceLastContact' in df:
        df['DaysSinceLastContact'] = df['DaysSinceLastContact'].fillna(0)
    if 'DaysSinceFirstContact' in df:
        df['DaysSinceFirstContact'] = df['DaysSinceFirstContact'].fillna(0)

    return df


def impute_nas_and_save_imputer(df,columns_to_impute):
    df_impute = df[columns_to_impute]
    logger.info(f"Imputing NAs in {columns_to_impute}")
    logger.info(f"NAs in DataFrame before imputation:")
    nna = df_impute.isna().sum()
    logger.info(f"{nna}")

    logger.info("No imputer provided, instancing and fitting a new one")
    imp = IterativeImputer(missing_values=np.nan,
                            sample_posterior=False,
                            max_iter=10,
                            tol=0.01,
                            initial_strategy='mean',
                            estimator=BayesianRidge())

    imp.fit(df_impute)
    logger.info("Creating new imputer")
    df_impute = pd.DataFrame(data=imp.transform(df_impute),
                             columns=df_impute.columns)

    logger.info(f"NAs in DataFrame after imputation:")
    nna = df_impute.isna().sum()
    logger.info(f"{nna}")

    # Assign column
    for column in columns_to_impute:
        df[column] = df_impute[column].to_numpy()
    del df_impute

    return df,imp


def impute_nas(df,columns_to_impute,imp):

    """Imputes NAs in fields of interest, using sklearn's Iterative imputer

    Args:
        df ([dataframe]): [Dataframe with the leads]
        columns_to_impute ([list of columns]): [List of strings with the columns to impute]

    Returns:
        df [dataframe]: [Dataframe with the leads]
    """
    df_impute = df[columns_to_impute]
    logger.info(f"Imputing NAs in {columns_to_impute}")
    logger.info(f"NAs in DataFrame before imputation:")
    nna = df_impute.isna().sum()
    logger.info(f"{nna}")
    # Instance the imputer if it is not created

    print("Using provided imputer")
    df_impute = pd.DataFrame(data=imp.transform(df_impute),
                             columns=df_impute.columns)

    logger.info(f"NAs in DataFrame after imputation:")
    nna = df_impute.isna().sum()
    logger.info(f"{nna}")

    # Assign column
    for column in columns_to_impute:
        df[column] = df_impute[column].to_numpy()
    del df_impute

    return df


def log_transformation(df, columns):
    """Transform selected variables using log, imputing mean in negative values to avoid errors

    Args:
        df ([dataframe]): [datafram with the leads]
        columns ([list of strings]): [list of the columns to transform]
    Returns:
        df ([dataframe]): [datafram with the leads]
    """
    for column in columns:
        logger.info(f'Log Transforming : {column}')
        df.loc[(df[column] < 0), column] = df[column].mean()
        df[column] = df[column].apply(lambda x: np.log10(x + 1))
    return df


def create_month_status(df):
    logger.info("Creating Month of the date column")
    if 'campaign_bulk_date' in df.columns:

        df['MonthStatus'] = pd.DatetimeIndex(
            df['campaign_bulk_date']).month.astype('int16')
        df['MonthStatus'] = df['MonthStatus'].astype("category")
    return df


def clean_companyfollowers_text(df):
    """Deletes any word in the CompanyFollowers field, and converts to float

    Args:
        df ([dataframe]): dataframe with the leads

    Returns:
        df[dataframe]: [dataframe with the leads]
    """

    df['CompanyFollowers'] = df['CompanyFollowers'].str.extract(
        '(\d+)', expand=False).astype('float')
    return df


def clean_mxtype(df,mxtypes):
    """

    :param df: Input Dataset
    :param mxtypes: MXTypes to maintain ( the rest will go to others)
    :return df: processed Dataset
    """

    if 'MXType' not in df.columns:
        raise Exception ("MXType column not preset ( Check Caps)")
    logger.info('Defining MXTypes')
    logger.info(f'legal MXTypes: {mxtypes}')
    df.loc[~df['MXType'].isin(mxtypes), 'MXType'] = 'Others'
    logger.info(f'{df.MXType.value_counts()}')
    return df


def clean_mxtype_using_dictionary(df,mx_bv_dict,mx_prob_dict):
    """

    :param df: Input Dataset
    :param mx_bv_dict: MXTypes dictionary by bv performance
    :param mx_prob_dict: MXTypes dictionary by prob performance
    :return df: processed Dataset
    """

    if 'MXType' not in df.columns:
        raise Exception ("MXType column not preset ( Check Caps)")
    logger.info('Defining MXTypes')
    df['mx_bv'] = df['MXType']
    df = df.replace({'mx_bv': mx_bv_dict})
    logger.info(f'{df.mx_bv.value_counts()}')
    df['mx_prob'] = df['MXType']
    df = df.replace( {'mx_prob': mx_prob_dict} )
    logger.info(f'{df.mx_prob.value_counts()}')
    return df


def create_new_position_flag(df,days):
    if 'DaysSincePositionStart' in df:
        logging.info(f'Days Since position detected, creating flag for {days} days')
        df['DaysSincePositionStart'].fillna(999)
        colname = 'new_position_'+str(days)
        df[colname] = 0
        df.loc[df['DaysSincePositionStart']< days,colname] = 1
        logging.info(f'{df[colname].value_counts()}')
    else:
        logging.info(' dayssincepositionstart Column not found, no changes were made.')
    return df
