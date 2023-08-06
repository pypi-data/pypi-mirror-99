from cygnsslib.CygDdmId import CygDdmId
import numpy as np
import os
import pandas as pd


def find_land_prod_sample_id_from_excel(xls_in, xls_out=None, start_col=1, st_row=1, out_sheet_suffix='', land_samp_col=None, timestamp_col=None):
    """

    Read the first sheet and the col. start_col to start_col+4.

    The output file is all the cells with new column: land_sample_zero_based

    :param xls_in: input Excel file
    :type xls_in: str
    :param xls_out: output Excel file name, if None add "_land_prod" to the file
    :type xls_out: str or None
    :param start_col: starting col. the function read start_col to start_col+4
    :type start_col: int
    :param st_row: Starting row, default 1 which is the header
    :type st_row: int
    :param out_sheet_suffix: suffix of the sheet name (NOT file name)
    :type out_sheet_suffix: str
    :param land_samp_col: col number of land_sample_zero_based, if None the default is start_col + 5
    :type land_samp_col: int or None
    :param timestamp_col: write the timestamp to tis col. if None the function will not write the timestamp
    :type timestamp_col: int or None
    :return: output file name
    :rtype: str
    """
    if xls_out is None:
        inxls_list = xls_in.split('.')
        xls_out = f'{inxls_list[0]:s}_land_prod.xlsx'  # car read xlsx and xls but write only to xls

    if not os.path.exists(xls_in):
        raise FileExistsError(f"Input Excel file doesn't exist, {xls_in:s}")
    df = pd.read_excel(xls_in)

    land_samp_list = []
    for i_ddm in df.itertuples():
        try:
            ddm_id = CygDdmId(None, i_ddm.year, i_ddm.day, i_ddm.flight_model, i_ddm.channel, i_ddm.sample_zero_based)
        except AttributeError:
            ddm_id = CygDdmId(None, i_ddm[start_col+1], i_ddm[start_col+2], i_ddm[start_col+3], i_ddm[start_col+4], i_ddm[start_col+5])
        try:
            ddm_id.fill_land_parameters()
        except:
            ddm_id.land_samp_id = None
        land_samp_list.append(ddm_id.land_samp_id)

    if land_samp_col is None or land_samp_col < 0:
        try:
            land_samp_col = int(np.where('sample_zero_based' == df.columns)[0][0] + 1)
        except IndexError:
            land_samp_col = start_col + 5
    df.insert(land_samp_col, 'land_sample_zero_based', land_samp_list)
    df.to_excel(xls_out, index=False)


if __name__ == '__main__':
    xls_in = 'SLV_Z4_thawed_2019.xlsx'
    find_land_prod_sample_id_from_excel(xls_in, xls_out=None, start_col=1, out_sheet_suffix='', timestamp_col=0)
    xls_in = 'SLV_Z1_thawed_2019.xlsx'
    find_land_prod_sample_id_from_excel(xls_in, xls_out=None, st_row=1, start_col=1, out_sheet_suffix='', timestamp_col=0)
