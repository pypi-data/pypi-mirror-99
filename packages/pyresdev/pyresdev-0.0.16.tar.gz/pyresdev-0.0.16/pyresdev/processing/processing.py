import pyresdev.utils._developer_utils as devutils
import pyresdev.utils as utils

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
__all__ = ['preprocessing_training']


def preprocessing_training_common(df, config, industry_dictionary, state_dictionary,
                                  mx_prob_dictionary, mx_bv_dictionary, model_type):
    """Common functions used for every campaign in the processing

    Args:
        df ([DataFrame]): [Dataframe to split]
        config ([Dict]): [Config for the campaign]
        Industry_dictionary ([dict]): [Industry dictionary]
        mx_prob_dictionary(dict) : MX dictionary converting to lead performance
        mx_bv_dictionary(dict) : MX Dictionary converting to bv performance
        state_dictionary(dict): state dictionary converting to bv performance
        model_type(dict): model used ( bv, probabiltiy or multiclass)
    Returns:
        [DataFrames]: [Training and testing divided into dependent and independent variables ]
    """
    # Set Types
    df = devutils.set_dataframe_columntypes( df )

    logging.info(f'{df.dtypes}')
    # Delete some statuses in training cases and create target column, set index in prediction cases
    status_to_delete = config['status_to_delete']
    df = devutils.clean_previous_status( df=df, status_to_clean=status_to_delete )

    # Eliminate rows with NA in the following columns ( the have a few NA)
    cols_to_clean_na = config['cols_to_clean_na']
    df = devutils.clean_rows_with_na( df=df, cols_to_clean_na=cols_to_clean_na )

    # Map industry dictionary
    df['Industry'] = df['Industry'].map(industry_dictionary)
    logging.info( df['Industry'].value_counts() )

    # Fill NA with "Uknown" in the  columns specified in the config
    cols_to_fill = config['fill_unknown']
    df = devutils.fill_na_with_unknown( df=df, columns=cols_to_fill )

    df = devutils.clean_mxtype_using_dictionary( df=df, mx_bv_dict=mx_bv_dictionary,
                                                 mx_prob_dict=mx_prob_dictionary )

    # map states dictionary
    df['State'] = df['State'].map( state_dictionary )
    logging.info( df['State'].value_counts() )

    # add the month of the transaction
    df = devutils.create_month_status( df=df )

    # Create Company years column
    df = devutils.create_company_years_column( df=df )

    for days in config['days_to_define_new_position']:
        df = devutils.create_new_position_flag(df=df, days=days)

    # Create new seniorities and the rest go to "other"
    df = devutils.fill_seniority_column( df=df )

    # Take the countries of the campaign from the config file
    countries_list = config['countries_list']
    df = devutils.filter_countries( df=df, countries=countries_list )

    # Fix errors in CompanyFollowers
    df = devutils.clean_companyfollowers_text( df=df )

    # Converting kw_key and technologies list of words to an int, using regex
    df = devutils.convert_kwkey_specialties_and_technologies_to_int( df=df )

    # Historic variables, fill nulls with 0
    df = devutils.fill_historic_variables( df=df )

    # Use imputer
    impute_columns = config['impute_columns']
    df_leads_clean, imp = devutils.impute_nas_and_save_imputer( df=df, columns_to_impute=impute_columns )
    imputer_name = config['imputer_name']
    imputer_output_path = os.path.join( '/opt/ml/processing/imputer', imputer_name )
    logging.info( 'Saving iterative imputer to {}'.format( imputer_output_path ) )
    pickle.dump( imp, open( imputer_output_path, 'wb' ) )

    # Logs
    cols_to_transform = config['cols_to_transform']
    df = devutils.log_transformation( df_leads_clean, columns=cols_to_transform )

    # Dropping unused variables
    print( model_type )
    cols_to_drop = config['cols_to_drop'][model_type]
    df = utils.drop_columns( df=df, columns=cols_to_drop )

    return df



def preprocessing_training(df, industry_dictionary, state_dictionary,
                           mx_bv_dictionary, mx_prob_dictionary, config, model_type):
    """[Pre-processing function to prepare the data for training the model and to make predictions]

    Args:
        df ([Pandas Dataframe]): [Pandas Dataframe with the raw data ]
        industry_dictionary ([Dict]): [Dictionary to reduce the cardinality of the "Industry attribute"]
        config(dict) : Dictionary with the configuration ( read from json)
        model_type(string) : type of the model to be used
        mx_bv_dictionary(string): Dictionary of MX converting to bv performance
        mx_prob_dictionary(string): Dictionary of MX converting to prob performance
        model_type(string) : can be probability, bv or multiclass
    Returns:
        df_clean[Pandas Dataframe]: Pre-processed DataFrame ready for training purposes
    """

    # Make a copy of the dataset
    df_leads_clean = df.copy()

    nna = df_leads_clean.isna().sum()
    logging.info( f"NA in original dataframe:" )
    logging.info( f"{nna}" )

    df_leads_clean = preprocessing_training_common( df=df_leads_clean,
                                                    config=config,
                                                    industry_dictionary=industry_dictionary,
                                                    mx_prob_dictionary=mx_prob_dictionary,
                                                    mx_bv_dictionary=mx_bv_dictionary,
                                                    state_dictionary=state_dictionary,
                                                    model_type=model_type )

    df_leads_clean = utils.reduce_mem_usage_category( df=df_leads_clean )
    df_leads_clean = utils.one_hot_encoding( df=df_leads_clean )

    # Prepare target column
    df_leads_clean = devutils.set_target_column(df=df_leads_clean,model_type=model_type,bins=config['bins'])

    nna = df_leads_clean.isna().sum()
    logging.info( f"NA in final dataframe:" )
    logging.info( f"{nna}" )

    return df_leads_clean
