from meteva.base import IV
import datetime
import numpy as np
import copy
import meteva
import collections
import os
import xarray as xr
import pandas as pd


# 参数数组转换为列表
def para_array_to_list(key_num, para_array):
    key_list = []
    for key in para_array.keys():
        key_list.append(key)
    key_count = len(key_list)

    if (key_num == key_count - 1):
        key = key_list[key_num]
        para_list = []
        list1 = para_array[key]
        for para in list1:
            dict1 = {}
            dict1[key] = para
            para_list.append(dict1)
    else:
        key = key_list[key_num]
        list1 = para_array[key]
        para_list0 = para_array_to_list(key_num + 1, para_array)
        para_list = []
        for para in list1:
            for dict0 in para_list0:
                dict1 = {}
                dict1[key] = para
                for key0 in dict0.keys():
                    dict1[key0] = copy.deepcopy(dict0[key0])
                # print(dict1)
                para_list.append(dict1)
    return para_list


def get_time_dims(para, is_fold_area=True):  # mpara, data_name_list,
    '''
    获取区域维度的名字和维度
    :param para: 最初的字典
    :param is_fold_time: 是否关闭time维度
    :return:
    '''
    group_set = copy.deepcopy(para['group_set'])
    # 获取维度信息
    if is_fold_area:
        group_set = close_area_grouping(group_set)
    coords = {}
    shape = []
    for coord in group_set.keys():
        if group_set[coord] != "fold":
            coords[coord] = ['、'.join(lable) for lable in group_set[coord]["group_name"]]
            shape.append(len(coords[coord]))
    return coords, shape


def close_area_grouping(group_dict):
    time_name_list = ['time', 'year', "month", "xun", "hou", "day", "hour", 'dtime']
    for key in group_dict:
        if key not in time_name_list:
            group_dict[key] = 'fold'
    return group_dict


# 迭代更新
def get_middle_veri_para(veri_para):
    nead_hmfc_methods = ["ts", "bias", "ets", "fal_rate", "hit_rate", "mis_rate"]
    nead_abcd_methods = ["pc", "spc"]
    nead_tase_methods = ['me', 'mae', 'mse', 'rmse']
    nead_toar_methods = ['mre']
    nead_tmmsss_methods = ['corr']
    mpara = copy.deepcopy(veri_para)
    methods = veri_para["method"]
    for method in methods:
        if method in nead_hmfc_methods:
            mpara["method"] = ["hmfn"]
            break
        if method in nead_abcd_methods:
            mpara["method"] = ["abcd"]
            break
        if method in nead_tase_methods:
            mpara["method"] = ["tase"]
            break
        if method in nead_toar_methods:
            mpara["method"] = ["toar"]
        if method in nead_tmmsss_methods:
            mpara['method'] = ['tmmsss']

    return mpara


def get_dims_and_coords_and_shape(para, shape, dims, indexes_dict, coords_dict, final_result_dict_list_array):
    new_coords_dict = {}
    new_indexes_dict = {}
    new_shape_dict = {}

    for i in range(len(para['veri_set'])):
        overall_shape = copy.deepcopy(shape)
        new_coords = []
        new_indexes = []
        for key in dims.keys():
            new_coords.append(dims[key])
            new_indexes.append(key)
        new_indexes.append('vmethod')
        new_indexes.extend(indexes_dict[i])
        new_coords.append(para['veri_set'][i]['method'])
        new_coords.extend(coords_dict[i])
        new_coords_dict[i] = new_coords
        new_indexes_dict[i] = new_indexes
        final_result_dict_list_array[i] = np.array(final_result_dict_list_array[i])
        area_shape = final_result_dict_list_array[i].shape[1:]
        overall_shape.extend(area_shape)
        new_shape_dict[i] = overall_shape
    return new_indexes_dict, new_coords_dict, new_shape_dict


def group_para(para_group_set):
    para_dict_list_list = {}
    for key in para_group_set:
        if para_group_set[key] != "fold" and para_group_set[key] != 'unfold':
            para_dict_list_list[key] = para_group_set[key]["group"]
            # para_dict_list_list ={dtime:[[],[],[]],dim_type_region:[[],[],[]]}
    if len(para_dict_list_list) < 1:
        para_list_dict_list = None
    else:
        para_list_dict_list = para_array_to_list(0, para_dict_list_list)
    return para_list_dict_list


def ob_time_and_fo_time_link(fo_start_time, fo_end_time, dtime_list, ob_time_dict, time_step):
    '''
    将实况时间==（预报时间+dtime) 的时间通过字典联系在一起如：
    {实况时间：[预报时间,dtime]}
    :param fo_start_time: 开始的预报时间
    :param fo_end_time: 结束预报时间
    :param dtime_list:  dtime的列表
    :param ob_time_dict: 实况时间的字典
    :param time_step: time跳跃的时间
    :return:
    '''
    time1 = copy.deepcopy(fo_start_time)
    while time1 <= fo_end_time:
        for dh in dtime_list:
            ob_time = time1 + datetime.timedelta(hours=dh)
            if ob_time not in ob_time_dict.keys():
                ob_time_dict[ob_time] = [[time1, dh]]
            else:
                ob_time_dict[ob_time].append([time1, dh])
        time1 = time1 + datetime.timedelta(hours=time_step)


# 迭代更新
def one_score(para, param, mid_result_list_set, sum):
    score_list = []
    area_indexes = []
    coords = []

    if 'ts' in param['method']:
        hmfn_sum = np.zeros((1))

        for data in mid_result_list_set:

            hmfn_data_array = data.hmfn_array
            area_indexes = list(hmfn_data_array.coords)[:-1]
            coords = []
            for index in area_indexes:
                label = hmfn_data_array[index].values
                coords.append(label)
            hmfn_array = hmfn_data_array.values
            hmfn_sum = hmfn_array + hmfn_sum

        hit = hmfn_sum[..., 0]
        mis = hmfn_sum[..., 1]
        fal = hmfn_sum[..., 2]
        ts = hit / (mis + fal + hit + 1e-6)
        score_list.append(ts)

    if 'bias' in param['method']:
        hmfn_sum = np.zeros((1))
        for data in mid_result_list_set:
            hmfn_data_array = data.hmfn_array
            area_indexes = list(hmfn_data_array.coords)[:-1]
            coords = []
            for index in area_indexes:
                label = hmfn_data_array[index].values
                coords.append(label)
            hmfn_array = hmfn_data_array.values
            hmfn_sum = hmfn_array + hmfn_sum
        hit = hmfn_sum[..., 0]
        mis = hmfn_sum[..., 1]
        fal = hmfn_sum[..., 2]
        bias = (hit + fal) / (mis + hit + 1e-6)
        score_list.append(bias)

    if 'pc' in param['method']:
        abcd_sum = np.zeros((1))

        for data in mid_result_list_set:
            abcd_data_array = data.abcd_array
            # print(abcd_data_array)
            area_indexes = list(abcd_data_array.coords)[:-1]
            coords = []
            for index in area_indexes:
                label = abcd_data_array[index].values
                coords.append(label)

            abcd_array = abcd_data_array.values
            abcd_sum = abcd_array + abcd_sum
        na = abcd_sum[..., 0]
        nd = abcd_sum[..., 3]
        pc = (na + nd) / (sum + 1e-6)

        score_list.append(pc)
    if 'me' in param['method']:
        tase_sum = np.zeros((1))
        for data in mid_result_list_set:
            tase_data_array = data.tase_array
            # print(list(tase_data_array.coords))
            area_indexes = list(tase_data_array.coords)[:-1]

            for index in area_indexes:
                label = tase_data_array[index].values
                coords.append(label)
            tase_array = tase_data_array.values
            tase_sum = tase_array + tase_sum
        me = tase_sum[..., 0] / (sum + 1e-6)
        score_list.append(me)
    if 'mae' in param['method']:
        tase_sum = np.zeros((1))
        for data in mid_result_list_set:
            tase_data_array = data.tase_array
            area_indexes = list(tase_data_array.coords)[:-1]
            coords = []
            for index in area_indexes:
                label = tase_data_array[index].values
                coords.append(label)
            tase_array = tase_data_array.values
            tase_sum = tase_array + tase_sum
        mae = tase_sum[..., 1] / (sum + 1e-6)
        score_list.append(mae)
    if 'mse' in param['method']:
        tase_sum = np.zeros((1))
        for data in mid_result_list_set:
            tase_data_array = data.tase_array
            area_indexes = list(tase_data_array.coords)[:-1]
            coords = []
            for index in area_indexes:
                label = tase_data_array[index].values
                coords.append(label)
            tase_array = tase_data_array.values
            tase_sum = tase_array + tase_sum
        mse = tase_sum[..., 2] / (sum + 1e-6)
        score_list.append(mse)
    if 'rmse' in param['method']:
        tase_sum = np.zeros((1))
        for data in mid_result_list_set:
            tase_data_array = data.tase_array

            area_indexes = list(tase_data_array.coords)[:-1]
            coords = []
            for index in area_indexes:
                label = tase_data_array[index].values
                coords.append(label)
            tase_array = tase_data_array.values
            tase_sum = tase_array + tase_sum

        mse = tase_sum[..., 2] / (sum + 1e-6)
        rmse = np.sqrt(mse)
        score_list.append(rmse)
    if 'mre' in param['method']:

        toar_sum = np.zeros((1))
        for data in mid_result_list_set:
            toar_data_array = data.toar_array

            area_indexes = list(toar_data_array.coords)[:-1]
            coords = []
            for index in area_indexes:
                label = toar_data_array[index].values
                coords.append(label)
            toar_array = toar_data_array.values
            toar_sum = toar_array + toar_sum

        count = toar_sum[..., 0] + 0
        if count.size == 1:
            if count == 0:
                mre0 = IV
            else:
                mre0 = toar_sum[..., 1] / count
        else:
            count[count < 0] = 1e-10
            ar = toar_sum[..., 1]
            mre0 = ar / count
            mre0[count < 1] = IV
        score_list.append(mre0)
    if 'corr' in param['method']:

        one_index = mid_result_list_set[0]['tmmsss_array'].shape
        model_num = len(para['forecasts'])
        tms_array = np.zeros(one_index)
        for i, data in enumerate(mid_result_list_set):
            tmmsss_data_array = data.tmmsss_array
            area_indexes = list(tmmsss_data_array.coords)[:-1]
            coords = []
            for index in area_indexes:
                label = tmmsss_data_array[index].values
                coords.append(label)

            tmmsss_array = tmmsss_data_array.values.reshape((-1, one_index[-1], one_index[-1]))

            one_new_index = tmmsss_array.shape[0]
            for one_new_i in range(one_new_index):
                for j in range(model_num):
                    a = tms_array[one_new_i, j, :]
                    b = tmmsss_array[one_new_i, j, :]
                    if np.all(b) == 0:
                        continue
                    tms_array[one_new_i, j, :] = tmmsss_merge(a, b)
                    # print(tms_array)

        # print(np.isnan(tms_array))

        sxx = tms_array[..., 3]
        syy = tms_array[..., 4]
        sxy = tms_array[..., 5]
        sxxsyy = np.sqrt(sxx * syy)
        if sxxsyy.size == 1:
            if sxxsyy == 0:
                sxxsyy = 1e-10
        else:
            sxxsyy[sxxsyy == 0] = 1e-10
        corr = sxy / sxxsyy
        corr = corr.reshape(one_index[:-1])

        score_list.append(corr)
    return score_list, area_indexes, coords


def create_DataArray_dict(para, final_result_dict_list_array, new_shape_dict, new_coords_dict, new_indexes_dict):
    # 将数据通过上文得到的indexes# coords和shape和grades转化为DataArray 并且将dataArray放到字典中

    all_catrgory_grades_data_array_dict = {}
    for i in range(len(para['veri_set'])):
        category_of_grades = final_result_dict_list_array[i]

        category_of_shape = new_shape_dict[i]
        category_of_coords = new_coords_dict[i]
        category_of_indexes = new_indexes_dict[i]
        category_of_grades = category_of_grades.reshape(category_of_shape)
        category_of_data_array = xr.DataArray(category_of_grades, coords=category_of_coords, dims=category_of_indexes)
        all_catrgory_grades_data_array_dict[i] = category_of_data_array
    return all_catrgory_grades_data_array_dict


def filter_valid_data(one_tiem_group_and_dtime_path):
    sum = np.zeros((1))
    data_list = []
    for path in one_tiem_group_and_dtime_path:
        data = xr.open_dataset(path)

        total_dataset = data['total_num']
        data_list.append(data)
        total_array = total_dataset.values
        sum = total_array + sum
    new_sum = copy.deepcopy(sum)
    new_sum[new_sum > 0] = -1
    new_sum += 1

    # 通过total 和total判断是否跳过该数据
    mid_result_list_set = []
    for data in data_list:
        total_dataset = data['total_num']
        total_array = total_dataset.values
        xx = new_sum + total_array
        if np.any(xx) == 0:
            continue
        else:
            mid_result_list_set.append(data)
    return mid_result_list_set, sum


def calculate_score(para, all_path, final_result_dict_list_array, indexes_dict, coords_dict):
    # tms_array = np.zeros((len(all_path), 6))
    for one_time_group_path in all_path:
        for one_tiem_group_and_dtime_path in one_time_group_path:

            mid_result_list_set, sum = filter_valid_data(one_tiem_group_and_dtime_path)

            # print(mid_result_list_set)
            # 获取area的indexes 和coords
            for i in range(len(para["veri_set"])):
                score_list, area_indexes, coords = one_score(para, para["veri_set"][i], mid_result_list_set, sum)
                final_result_dict_list_array[i].append(score_list)
                indexes_dict[i] = area_indexes
                coords_dict[i] = coords

    return final_result_dict_list_array, coords_dict, indexes_dict


def filter_time_series(par_dict, time_Series2):
    if par_dict != 0:
        for key in par_dict.keys():
            if key == "year":
                time_series1 = pd.Series()
                for year in par_dict[key]:
                    time_Series0 = time_Series2.loc[time_Series2.dt.year == year]
                    time_series1 = time_series1.append(time_Series0)
                time_Series2 = time_series1
            if key == "month":
                time_series1 = pd.Series()
                for month in par_dict[key]:
                    time_Series0 = time_Series2.loc[time_Series2.dt.month == month]
                    time_series1 = time_series1.append(time_Series0)
                time_Series2 = time_series1
            if key == "xun":
                time_series1 = pd.Series()
                for xun in par_dict[key]:
                    mons = time_Series2.map(lambda x: x.month).values.astype(np.int16)
                    days = time_Series2.map(lambda y: y.day).values.astype(np.int16)
                    xuns = np.ceil(days / 10).astype(np.int16)
                    xuns[xuns > 3] = 3
                    xuns += (mons - 1) * 3
                    time_Series0 = time_Series2.loc[xuns == xun]
                    time_series1 = time_series1.append(time_Series0)
                time_Series2 = time_series1
            if key == "hou":
                time_series1 = pd.Series()
                for hou in par_dict[key]:
                    mons = time_Series2.map(lambda x: x.month).values.astype(np.int16)
                    days = time_Series2.map(lambda y: y.day).values.astype(np.int16)
                    hous = np.ceil(days / 5).astype(np.int16)
                    hous[hous > 6] = 6
                    hous += (mons - 1) * 6
                    time_Series0 = time_Series2.loc[hous == hou]
                    time_series1 = time_series1.append(time_Series0)
                time_Series2 = time_series1

            if key == "day":
                time_series1 = pd.Series()
                # print(time_Series2)
                for day in par_dict[key]:
                    # print(time_Series2.dt.day==day)
                    time_Series0 = time_Series2.loc[time_Series2.dt.day == day]
                    time_series1 = time_series1.append(time_Series0)

                time_Series2 = time_series1

            if key == "hour":
                time_series1 = pd.Series()
                for hour in par_dict[key]:
                    time_Series0 = time_Series2.loc[time_Series2.dt.hour == hour]
                    time_series1 = time_series1.append(time_Series0)
                time_Series2 = time_series1
    return time_Series2


def join_time_dtime_nc_path(dtime_group_list_list, time_df):
    one_time_group_path = []
    for dtime_group_list in dtime_group_list_list:
        dtime_group_list = ['%03d' % dtime for dtime in dtime_group_list]
        dtime_df = pd.DataFrame({'dtime': dtime_group_list})
        dtime_df['value'] = 1
        # 通过merge进行笛卡尔积运算
        one_tiem_group_and_dtime_df = pd.merge(time_df, dtime_df, on='value')
        one_tiem_group_and_dtime_df['time'] = one_tiem_group_and_dtime_df['time'].apply(
            lambda x: x.strftime('%Y%m%d%H'))
        one_tiem_group_and_dtime_df['nc'] = 'nc'
        one_tiem_group_and_dtime_df = one_tiem_group_and_dtime_df.drop(['value'], axis=1)
        one_tiem_group_and_dtime_list_list = one_tiem_group_and_dtime_df.values.tolist()
        # 将笛卡尔积得到的df转化为的列表进行join 从而拼接成path
        one_tiem_group_and_dtime_path = ['.'.join(one_tiem_group_and_dtime_list) for
                                         one_tiem_group_and_dtime_list in
                                         one_tiem_group_and_dtime_list_list]
        one_time_group_path.append(one_tiem_group_and_dtime_path)
    return one_time_group_path


def get_all_path(para, para_dict_list_list, time_Series, dtime_list, shape):
    all_path = []
    for par_dict in para_dict_list_list:
        time_Series2 = copy.deepcopy(time_Series)
        # 通过time分组来进行对time进行筛选，挑选出符合当前分组的time
        time_Series2 = filter_time_series(par_dict, time_Series2)

        # 对分组dtime和上文筛选出的time进行笛卡尔积
        time_df = pd.DataFrame({'time': time_Series2})  # 将时间series转化为df是为了下一步笛卡尔积运算
        time_df['value'] = 1
        if para['group_set']['dtime'] == 'fold':
            dtime_group_list_list = [dtime_list]
            shape.append(len(dtime_group_list_list))
        elif para['group_set']['dtime'] == 'unfold':
            dtime_array = np.array(dtime_list)
            dtime_array = dtime_array.reshape([-1, 1])
            dtime_group_list_list = dtime_array.tolist()
            shape.append(len(dtime_group_list_list))
        else:
            dtime_group_list_list = para['group_set']['dtime']['group']
        one_time_group_path = join_time_dtime_nc_path(dtime_group_list_list, time_df)

        all_path.append(one_time_group_path)
    return all_path, shape


def create_empty_data_and_coords_and_indexes_dict(para):
    final_result_dict_list_array = {}
    coords_dict = {}
    indexes_dict = {}
    for i in range(len(para["veri_set"])):
        final_result_dict_list_array[i] = []
        coords_dict[i] = None
        indexes_dict[i] = None
    return final_result_dict_list_array, coords_dict, indexes_dict


def get_time_Series(time1, fo_end_time, time_type, time_step):
    time_list = []
    # 对时间序列进行处理
    time_Series = None
    while time1 <= fo_end_time:
        if time_type == "h":
            time1 = time1 + datetime.timedelta(hours=time_step)
        else:
            time1 = time1 + datetime.timedelta(minutes=time_step)
        time_list.append(time1)
        time_Series = pd.Series(time_list)
    return time_Series


def time_unfold(para, time_series):
    new_time_series = copy.deepcopy(time_series)
    for key in para['group_set'].keys():
        if key == 'year' and para['group_set'][key] == 'unfold':
            year_series = new_time_series.dt.year
            year_list = list(set(year_series))
            year_np = np.array(year_list)

            year_np = year_np.reshape([-1, 1])
            year_list_list = year_np.tolist()
            para['group_set'][key] = {}
            para['group_set'][key]['group'] = year_list_list
            new_year_list_list = copy.deepcopy(year_list_list)
            group_name_list_list = []
            for year_list in new_year_list_list:
                group_name_list = []
                for year in year_list:
                    year_name = str(year) + '年'

                    group_name_list.append(year_name)
                group_name_list_list.append(group_name_list)
            para['group_set'][key]['group_name'] = group_name_list_list

        if key == 'month' and para['group_set'][key] == 'unfold':
            month_series = new_time_series.dt.day
            month_list = list(set(month_series))
            month_np = np.array(month_list)

            month_np = month_np.reshape([-1, 1])
            month_list_list = month_np.tolist()
            para['group_set'][key] = {}
            para['group_set'][key]['group'] = month_list_list
            new_month_list_list = copy.deepcopy(month_list_list)
            group_name_list_list = []
            for month_list in new_month_list_list:
                group_name_list = []
                for month in month_list:
                    month_name = str(month) + '月'

                    group_name_list.append(month_name)
                group_name_list_list.append(group_name_list)
            para['group_set'][key]['group_name'] = group_name_list_list

        if key == 'xun' and para['group_set'][key] == 'unfold':
            mons = new_time_series.map(lambda x: x.month).values.astype(np.int16)
            days = new_time_series.map(lambda y: y.day).values.astype(np.int16)
            xuns = np.ceil(days / 10).astype(np.int16)
            xuns[xuns > 3] = 3
            xuns += (mons - 1) * 3
            xun_list = list(set(xuns))
            xun_np = np.array(xun_list)

            xun_np = xun_np.reshape([-1, 1])
            xun_list_list = xun_np.tolist()
            para['group_set'][key] = {}
            para['group_set'][key]['group'] = xun_list_list
            new_xun_list_list = copy.deepcopy(xun_list_list)
            group_name_list_list = []
            for xun_list in new_xun_list_list:
                group_name_list = []
                for xun in xun_list:
                    xun_name = str(xun) + '旬'

                    group_name_list.append(xun_name)
                group_name_list_list.append(group_name_list)
            para['group_set'][key]['group_name'] = group_name_list_list

        if key == 'hou' and para['group_set'][key] == 'unfold':
            mons = new_time_series.map(lambda x: x.month).values.astype(np.int16)
            days = new_time_series.map(lambda y: y.day).values.astype(np.int16)
            hous = np.ceil(days / 5).astype(np.int16)
            hous[hous > 6] = 6
            hous += (mons - 1) * 6
            hous_list = list(set(hous))
            hous_np = np.array(hous_list)

            hous_np = hous_np.reshape([-1, 1])
            hous_list_list = hous_np.tolist()
            para['group_set'][key] = {}
            para['group_set'][key]['group'] = hous_list_list
            new_hous_list_list = copy.deepcopy(hous_list_list)
            group_name_list_list = []
            for hous_list in new_hous_list_list:
                group_name_list = []
                for hous in hous_list:
                    hous_name = str(hous) + '侯'

                    group_name_list.append(hous_name)
                group_name_list_list.append(group_name_list)
            para['group_set'][key]['group_name'] = group_name_list_list

        if key == 'day' and para['group_set'][key] == 'unfold':
            day_series = new_time_series.dt.day
            day_list = list(set(day_series))
            day_np = np.array(day_list)

            day_np = day_np.reshape([-1, 1])
            day_list_list = day_np.tolist()
            para['group_set'][key] = {}
            para['group_set'][key]['group'] = day_list_list
            new_day_list_list = copy.deepcopy(day_list_list)
            group_name_list_list = []
            for day_list in new_day_list_list:
                group_name_list = []
                for day in day_list:
                    day_name = str(day) + '日'

                    group_name_list.append(day_name)
                group_name_list_list.append(group_name_list)
            para['group_set'][key]['group_name'] = group_name_list_list

        if key == 'hour' and para['group_set'][key] == 'unfold':
            hour_series = new_time_series.dt.hour
            hour_list = list(set(hour_series))
            hour_np = np.array(hour_list)

            hour_np = hour_np.reshape([-1, 1])
            hour_list_list = hour_np.tolist()
            para['group_set'][key] = {}
            para['group_set'][key]['group'] = hour_list_list
            new_hour_list_list = copy.deepcopy(hour_list_list)
            group_name_list_list = []
            for hour_list in new_hour_list_list:
                group_name_list = []
                for hour in hour_list:
                    hour_name = str(hour) + '时'

                    group_name_list.append(hour_name)
                group_name_list_list.append(group_name_list)
            para['group_set'][key]['group_name'] = group_name_list_list
    return para


def cut_sta_not_after(sta, time):
    if sta is None:
        return None, None
    else:
        not_after_part = sta.loc[sta["time"] <= time]
        after_part = sta.drop(not_after_part.index)
        return not_after_part, after_part




# 通过指定参数获取站点信息
def get_sta_by_para(sta, para):
    sta1 = copy.deepcopy(sta)
    for key in para.keys():
        if key == "level":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_level_list(sta1, para[key])
        elif key == "time":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_time_list(sta1, para[key])
        elif key == "year":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_year_list(sta1, para[key])
        elif key == "month":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_month_list(sta1, para[key])
        elif key == "xun":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_xun_list(sta1, para[key])
        elif key == "hou":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_hou_list(sta1, para[key])
        elif key == "day":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_day_list(sta1, para[key])
        elif key == "hour":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_hour_list(sta1, para[key])
        elif key == "dtime":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_dtime_list(sta1, para[key])
        elif key == "dday":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_dday_list(sta1, para[key])
        elif key == "dhour":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_dhour_list(sta1, para[key])
        elif key == "dminute":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_dminute_list(sta1, para[key])
        elif key == "id":
            sta1 = meteva.base.function.get_from_sta_data.sta_in_id_list(sta1, para[key])
        elif key == 'lon':
            sta1 = meteva.base.function.get_from_sta_data.sta_between_lon_range(sta1, para[key][0],
                                                                                                 para[key][1])
        elif key == 'lat':
            sta1 = meteva.base.function.get_from_sta_data.sta_between_lat_range(sta1, para[key][0],
                                                                                                 para[key][1])
        elif key == "alt":
            sta1 = meteva.base.function.get_from_sta_data.sta_between_alt_range(sta1, para[key][0],
                                                                                                 para[key][1])
        else:

            if key in sta1.columns:
                # print(para[key])
                sta1 = sta1.loc[sta1[key].isin(para[key])]
            else:
                print("参数关键词不支持")
    return sta1


def close_time_grouping(group_dict):
    time_name_list = ['time', 'year', "month", "xun", "hou", "day", "hour", "dtime"]
    for key in group_dict:
        if key in time_name_list:
            group_dict[key] = 'fold'
    return group_dict


# 将数据按照规定的分组规则进行分成一个个小数据   并放到一个列表中
def group_sta(sta, para_group_set):
    para_dict_list_list = {}
    for key in para_group_set:
        if para_group_set[key] != "fold":
            para_dict_list_list[key] = para_group_set[key]["group"]
            # para_dict_list_list ={dtime:[[],[],[]],dim_type_region:[[],[],[]]}

    para_list_dict_list = para_array_to_list(0, para_dict_list_list)
    sta_list = []
    for para_dict_list in para_list_dict_list:
        sta1 = get_sta_by_para(sta, para_dict_list)
        sta_list.append(sta1)
        # print(len(sta_list))
    return sta_list, para_list_dict_list



def get_middle_veri_result(sta_list, para, area_coords, area_shape, model_coords, model_shape, one_veri_set_para_coords,
                           one_veri_set_para_shape, confusion_matrix_coords, confusion_matrix_shape):
    # para 是中间量检验的参数
    '''
    获取 一个hmfn或者abcd中的一个检验结果，和total_num 并将两个指标加入Data_set中
    :param sta_list:
    :param para:
    :param area_coords:
    :param area_shape:
    :param model_coords:
    :param model_shape:
    :param one_veri_set_para_coords:
    :param one_veri_set_para_shape:
    :param confusion_matrix_coords:
    :param confusion_matrix_shape:
    :return:
    '''

    sample_same = para["sample_must_be_same"]
    model_num = len(model_coords['member'])
    # print(data_name_list)
    data_names = copy.deepcopy(model_coords['member'])
    data_names.insert(0, 'ob')
    veri_list_4d = []
    total_num_list_list = []
    for sta in sta_list:
        total_num_list = []

        # 计算总的非9999样本数
        if sta is None or len(sta.index) == 0:
            for i in range(model_num):
                total_num_list.append(0)
        else:
            for i in range(model_num):
                model_name = model_coords['member'][i]
                fo = sta[model_name].values
                fo = fo[fo != 9999]
                total_num_list.append(len(fo))
        para1 = None
        para2 = None
        if "para1" in para.keys():
            para1 = para["para1"]
        if "para2" in para.keys():
            para2 = para["para2"]
        # Error

        for vmethod in para["method"]:
            result = ver_one_groupsta_one_method(sta, vmethod, para1, para2, data_names,
                                                 sample_same)
        veri_list_4d.append(result)
        total_num_list_list.append(total_num_list)
    veri_array_4d = np.array(veri_list_4d)
    total_num_array_2d = np.array(total_num_list_list)
    shape_list = []
    for shape in [area_shape, model_shape, one_veri_set_para_shape, confusion_matrix_shape]:
        shape_list.extend(shape)
    shape_array = np.array(shape_list)
    shape_array = shape_array[shape_array != None]
    shape_list = list(shape_array)

    veri_array = veri_array_4d.reshape(shape_list)
    shape_list = copy.deepcopy(area_shape)
    total_num_shape = shape_list.extend(model_shape)
    total_num_array = total_num_array_2d.reshape(total_num_shape)
    dim_label, dim_name = dim_name_and_label_splice(area_coords, model_coords)

    total_array = xr.DataArray(total_num_array,
                               coords=dim_label,
                               dims=dim_name)

    ds1 = xr.Dataset({'total_num': total_array})
    dim_label, dim_name = dim_name_and_label_splice(area_coords, model_coords, one_veri_set_para_coords,
                                                    confusion_matrix_coords)
    # 迭代更改
    if para["method"] == ['hmfn']:
        hmfn_array = xr.DataArray(veri_array_4d,
                                  coords=dim_label,
                                  dims=dim_name)
        ds2 = xr.Dataset({"hmfn_array": hmfn_array})
        ds1 = ds1.update(ds2)
    if para['method'] == ['abcd']:
        abcd_array = xr.DataArray(veri_array,
                                  coords=dim_label,
                                  dims=dim_name)
        ds2 = xr.Dataset({"abcd_array": abcd_array})
        ds1 = ds1.update(ds2)
    if para['method'] == ['tase']:
        tase_array = xr.DataArray(veri_array, coords=dim_label, dims=dim_name)

        ds2 = xr.Dataset({"tase_array": tase_array})
        ds1 = ds1.update(ds2)
    if para['method'] == ['toar']:
        toar_array = xr.DataArray(veri_array, coords=dim_label, dims=dim_name)
        ds2 = xr.Dataset({'toar_array': toar_array})

        ds1 = ds1.update(ds2)
    if para['method'] == ['tmmsss']:
        tmmsss_array = xr.DataArray(veri_array, coords=dim_label, dims=dim_name)
        ds2 = xr.Dataset({'tmmsss_array': tmmsss_array})
        ds1 = ds1.update(ds2)
    return ds1


def get_area_dims(para, is_fold_time=True):  # mpara, data_name_list,
    '''
    获取区域维度的名字和维度
    :param para: 最初的字典
    :param is_fold_time: 是否关闭time维度
    :return:
    '''
    group_set = copy.deepcopy(para['group_set'])
    # 获取维度信息
    if is_fold_time == True:
        group_set = close_time_grouping(group_set)
    coords = {}
    shape = []
    for coord in group_set.keys():
        if group_set[coord] != "fold":
            coords[coord] = group_set[coord]["group_name"]
            shape.append(len(coords[coord]))
    return coords, shape


def get_model_dims(data_name_list):
    # 获取模式维度的名字和形状
    '''
    :param data_name_list: 所有模式名字的list
    :return:
    '''
    shape = []
    coords = {}
    coords["member"] = data_name_list[1:]
    shape.append(len(coords['member']))
    return coords, shape


def get_one_veri_set_para_dims(one_veri_set_dict):
    '''
    获取一种veri_set的等级的name  和shape
    :param one_veri_set_dict:   一个veri_set 的字典比如   {
            "name": "ts_bias",
            "method": ["ts", "bias"],
            "para1": [0.1, 5, 10, 20],
            "para1Name": ["小雨", ">=5毫米", ">=10毫米", ">=20毫米"],
            "plot_type": "bar"
        }
    :return:
    '''
    shape = []
    coords = {}
    para1 = None
    if ("para1" in one_veri_set_dict.keys()):
        para1 = one_veri_set_dict["para1"]
        if (para1 is not None):
            shape.append(len(para1))
            coords["para1"] = para1
    if ("para2" in one_veri_set_dict.keys()):
        para2 = one_veri_set_dict["para2"]
        if (para1 is not None):
            shape.append(len(para2))
            coords["para2"] = para2

    return coords, shape


# 迭代更新
def get_confusion_matrix_dims(one_veri_set_dict):
    '''
    获取混淆矩阵的维度的名字  与hmfn   和 abcd 有关维度名字 和shape
    :param one_veri_set_dict: 一个veri_set 的字典比如   {
            "name": "ts_bias",
            "method": ["ts", "bias"],
            "para1": [0.1, 5, 10, 20],
            "para1Name": ["小雨", ">=5毫米", ">=10毫米", ">=20毫米"],
            "plot_type": "bar"
        }
    :return:
    '''
    coodrs = {}
    shape = []
    if one_veri_set_dict['method'] == ['hmfn']:
        coodrs = {'hmfn': ['hit', 'mis', 'fla', 'cn']}
        shape = [4]
    if one_veri_set_dict['method'] == ['abcd']:
        coodrs = {'abcd': ["na", "nb", "nc", "nd"]}
        shape = [4]
    if one_veri_set_dict['method'] == ['tase']:
        coodrs = {'tase': ['error_sum', 'total_absolute_error', 'sum_error_squares']}  # 总样本数、误差总和、绝对误差总和、误差平方总和
        shape = [3]
    if one_veri_set_dict['method'] == ['toar']:
        coodrs = {'toar': ['num_greater_than_zero', 'sum_of_absolute_relative_errors']}  # 大于0的样本数，相对误差绝对值总和
        shape = [2]
    if one_veri_set_dict['method'] == ['tmmsss']:
        coodrs = {'tmmsss': ['sample_size', ' observed_mean', 'forecast_mean', 'observed_variance', 'forecast_variance',
                             'covariance']}
        shape = [6]
    return coodrs, shape


# 迭代更新
def ver_one_groupsta_one_method(sta, vmethod, para1, para2, data_names, sample_same):
    fo_num = len(data_names) - 1
    result = []
    if sta is not None and len(sta.index) > 0:
        # print(len(sta.index))
        data = copy.deepcopy(sta[data_names].values)  # 取出数据
        # print(data.shape)
        # print(data)
        if sample_same:
            # 首先判断全为9999的模式个数
            all_9999_num = 0
            for i in range(fo_num):
                fo = data[:, i + 1]
                index = np.where(fo != 9999)
                # 当一列全为9999时 all_9999_num +1
                if len(fo[fo != 9999]) == 0:
                    all_9999_num += 1

            # 判断每一行为9999的数目是否等于 all_9999_num
            is_9999 = np.zeros(data.shape)
            is_9999[data != 9999] = 0
            is_9999[data == 9999] = 1
            # 对于那些非全为9999的行

            sum_is_9999 = np.sum(is_9999, axis=1)
            # 每一行为9999的数目等于all_9999_num的数据取出
            index = np.where(sum_is_9999 == all_9999_num)[0]
            data = data[index, :]  # 每行为缺省的模式与全部缺省的列数一致。相当于把缺省模式大于 全部缺省的列的数据删除

    for i in range(fo_num):
        result_one_model = None
        if sta is not None and len(sta.index) > 0:

            ob = data[:, 0]
            fo = data[:, i + 1]
            if not sample_same:
                ob = ob[fo != 9999]
                fo = fo[fo != 9999]

            if len(fo) > 0 and fo[0] != 9999:
                # print(fo[fo>1])
                if vmethod == "hmfn":
                    result_one_model = np.array(list(meteva.method.yes_or_no.score.hmfn
                                                     (ob, fo, para1)))
                    result_one_model = result_one_model.T
                elif vmethod == 'abcd':
                    result_one_model = np.array(list(meteva.method.yes_or_no.score.hmfn_of_sunny_rainy
                                                     (ob, fo)))
                    result_one_model = result_one_model.T

                elif vmethod == 'tase':
                    e_sum = np.sum(fo - ob)
                    ae_sum = np.sum(np.abs(fo - ob))
                    se_sum = np.sum(np.square(fo - ob))
                    result_one_model = np.array([e_sum, ae_sum, se_sum])
                elif vmethod == 'toar':
                    s = ob + fo
                    d = ob - fo
                    s1 = s[s > 0]
                    d1 = d[s > 0]
                    ar = np.sum(np.abs(d1 / s1))
                    result_one_model = np.array([s1.size, ar])

                elif vmethod == 'tmmsss':
                    result_one_model = tmmsss(ob, fo)

        if result_one_model is None:
            if vmethod == "hmfn":
                result_one_model = np.zeros((len(para1), 4))
            elif vmethod == 'abcd':
                result_one_model = np.zeros(4)
            elif vmethod == 'tase':
                result_one_model = np.zeros(3)
            elif vmethod == 'toar':
                result_one_model = np.zeros(2)
            elif vmethod == 'tmmsss':
                result_one_model = np.zeros(6)

        re_list = result_one_model.tolist()
        result.append(re_list)

    return result


# wwww
def tmmsss_merge(tmmsss0, tmmsss1):
    '''
    将两份包含样本数、平均值和方差、协方差的中间结果合并
    :param tmmsss0: 长度6的一维数组，分别记录了（count,mx,my,sxx,syy,sxy）
    :param tmmsss1: 长度6的一维数组，分别记录了（count,mx,my,sxx,syy,sxy）
    :return: 长度6的一维数组，分别记录了（count,mx,my,sxx,syy,sxy）
    '''
    count_0 = tmmsss0[..., 0]

    mx_0 = tmmsss0[..., 1]
    my_0 = tmmsss0[..., 2]
    sxx_0 = tmmsss0[..., 3]
    syy_0 = tmmsss0[..., 4]
    sxy_0 = tmmsss0[..., 5]
    count_1 = tmmsss1[..., 0]
    mx_1 = tmmsss1[..., 1]
    my_1 = tmmsss1[..., 2]
    sxx_1 = tmmsss1[..., 3]
    syy_1 = tmmsss1[..., 4]
    sxy_1 = tmmsss1[..., 5]
    _, _, sxx_total = ss_iteration(count_0, mx_0, sxx_0, count_1, mx_1, sxx_1)
    _, _, syy_total = ss_iteration(count_0, my_0, syy_0, count_1, my_1, syy_1)
    count_total, mx_total, my_total, sxy_total = sxy_iteration(count_0, mx_0, my_0, sxy_0,
                                                               count_1, mx_1, my_1, sxy_1)
    return np.array([count_total, mx_total, my_total, sxx_total, syy_total, sxy_total])


def sxy_iteration(count_old, meanx_old, meany_old, sxy_old, count_new, meanx_new, meany_new, sxy_new):
    import math
    count_total = count_new + count_old
    rate1 = count_old / count_total
    rate2 = count_new / count_total
    meanx_total = rate1 * meanx_old + rate2 * meanx_new
    meany_total = rate1 * meany_old + rate2 * meany_new
    sxy_total = sxy_old * count_old
    sxy_total += count_old * ((1 - rate1) * meanx_old - rate2 * meanx_new) * (
            (1 - rate1) * meany_old - rate2 * meany_new)
    sxy_total += sxy_new * count_new
    sxy_total += count_new * ((1 - rate2) * meanx_new - rate1 * meanx_old) * (
            (1 - rate2) * meany_new - rate1 * meany_old)
    sxy_total /= count_total
    return count_total, meanx_total, meany_total, sxy_total


def ss_iteration(count_old, mean_old, ss_old, count_new, mean_new, ss_new):
    import math
    count_total = count_new + count_old
    rate1 = count_old / count_total
    rate2 = count_new / count_total
    mean_total = rate1 * mean_old + rate2 * mean_new
    ss_total = ss_old * count_old
    ss_total += count_old * (((1 - rate1) * mean_old - rate2 * mean_new) ** 2)
    ss_total += ss_new * count_new
    ss_total += count_new * (((1 - rate2) * mean_new - rate1 * mean_old) ** 2)
    ss_total /= count_total
    return count_total, mean_total, ss_total


def tmmsss(Ob, Fo):
    '''
    统计相关系数等检验量所需的中间变量
    :param Ob: 实况数据  任意维numpy数组
    :param Fo: 预测数据 任意维numpy数组,Fo.shape 和Ob.shape一致
    :return: numpy 一维数组，其元素为根据Ob和Fo
    计算出的（样本数，观测平均值，预报平均值，观测方差，预报方差，协方差
    '''
    ob_f = Ob.flatten()
    fo_f = Fo.flatten()
    count = Ob.size
    mx = np.mean(ob_f)
    my = np.mean(fo_f)
    dx = ob_f - mx
    dy = fo_f - my
    sxx = np.mean(np.power(dx, 2))
    syy = np.mean(np.power(dy, 2))
    sxy = np.mean(dx * dy)
    return np.array([count, mx, my, sxx, syy, sxy])


def dim_name_and_label_splice(*coords):
    '''
    拼接shape  和name
    :param coords:  多个维度的coords
    :return:
    '''
    dim_label = []
    dim_name = []
    for dim in coords:
        for key in dim.keys():
            dim_label.append(dim[key])
            dim_name.append(key)
    return dim_label, dim_name


def read_ob_data(dtime_list, time1, ob_time_dict, para, station, value_s, value_e):
    ob_sta_all = None
    copy_ob_time_dict = copy.deepcopy(ob_time_dict)
    for dtime in dtime_list:
        ob_time = time1 + datetime.timedelta(hours=dtime)
        # print(ob_time)
        # print(ob_time_dict.keys())
        if ob_time in ob_time_dict.keys():
            path = meteva.base.tool.path_tools.get_path(para["observation"]["path"], ob_time)
            ob_sta = meteva.base.io.read_stadata.read_from_micaps3(path, station=station)

            if ob_sta is not None:
                ob_sta = meteva.base.function.get_from_sta_data.sta_between_value_range(ob_sta,
                                                                                                         value_s,
                                                                                                         value_e)
                time_dtime_list = copy_ob_time_dict[ob_time]
                for time_dtime in time_dtime_list:
                    # print(time_dtime)
                    ob_sta1 = copy.deepcopy(ob_sta)
                    time_p = time_dtime[0]
                    dtime = time_dtime[1]
                    meteva.base.set_time_dtime_level_name(ob_sta1, time=time_p, dtime=dtime,
                                                                           level=0, data_name="ob")
                    ob_sta_all = meteva.base.function.put_into_sta_data.join(ob_sta_all, ob_sta1)
            copy_ob_time_dict.pop(ob_time)

    return ob_sta_all, copy_ob_time_dict


def read_dim_type_data(dim_type_num, para_dim_type, dim_type_sta1_list, station, dtime_list, time1,
                       dim_type_sta_all_dict):
    for i in range(dim_type_num):

        sta = None
        if para_dim_type[i]["fix"]:

            if len(dim_type_sta1_list) > i:
                path = para_dim_type[i]["path"]
                if para_dim_type[i]["type"] == "grid_data":
                    grd = meteva.base.io.read_griddata.read_from_nc(path)
                    if grd is not None:
                        # 将格点插值到站点上
                        sta = meteva.base.function.gxy_sxy.interpolation_nearest(grd, station)
                else:
                    sta = meteva.base.io.read_stadata.read_from_micaps3(path, station)
            else:
                sta = copy.deepcopy(dim_type_sta1_list[i])
                dim_type_sta1_list.append(sta)
        else:
            dir = para_dim_type[i]["path"]
            path = meteva.base.tool.path_tools.get_path(dir, time1)
            if para_dim_type[i]["type"] == "grid_data":
                grd = meteva.base.io.read_griddata.read_from_nc(path)
                sta = meteva.base.function.gxy_sxy.interpolation_nearest(grd, station)
            else:
                sta = meteva.base.io.read_stadata.read_from_micaps3(path, station)

        for dtime in dtime_list:
            sta1 = copy.deepcopy(sta)

            meteva.base.set_time_dtime_level_name(sta1, time=time1, dtime=dtime, level=0,
                                                                   data_name=para_dim_type[i]["name"])
            dim_type_sta_all_dict[i] = meteva.base.function.put_into_sta_data.join(
                dim_type_sta_all_dict[i], sta1)


def read_fo_data_on_one_time_and_one_dtime(para, model_id, time1, dtime, station, value_s, value_e,
                                           fo_sta_on_one_time_and_onedtime_all_dict):
    '''
    :param para:
    :param model_id:
    :param time1:
    :param dtime:
    :param station:
    :param value_s:
    :param value_e:
    :param fo_sta_on_one_time_and_onedtime_all_dict:
    :return:
    '''
    i = model_id
    one_fo_para = para["forecasts"][i]
    data_name = one_fo_para["name"]

    range_b = one_fo_para["fo_time_move_back"]
    # 读取回退时间
    fo_time_move_backs = np.arange(range_b[0], range_b[1], range_b[2]).tolist()
    find_file = False
    path = None
    for move_back in fo_time_move_backs:
        time_model = time1 - datetime.timedelta(hours=move_back)
        dtime_model_max = dtime + move_back
        if one_fo_para["ob_time_need_be_same"]:
            dtime_model_try = [dtime_model_max]
        else:
            dtime_model_try = np.arange(dtime_model_max, -1, -1).tolist()
        for dtime_model in dtime_model_try:
            dtime_model_int = int(dtime_model)
            path = meteva.base.tool.path_tools.get_path(one_fo_para["path"], time_model,
                                                                         dtime_model_int)
            if os.path.exists(path):
                find_file = True
                break
        if find_file:
            break
    fo_sta = None
    if find_file:
        if one_fo_para["type"] == "sta_data":
            fo_sta = meteva.base.io.read_stadata.read_from_micaps3(path, station)
        else:
            grd = meteva.base.io.read_griddata.read_from_nc(path)
            if grd is not None:
                fo_sta = meteva.base.function.gxy_sxy.interpolation_nearest(grd, station)
                fo_sta = meteva.base.function.sxy_sxy.set_data_to(fo_sta, station)
    if fo_sta is None:
        fo_sta = copy.deepcopy(station)
    fo_sta = meteva.base.function.sxy_sxy.set_value_out_9999(fo_sta, value_s, value_e)
    meteva.base.set_time_dtime_level_name(fo_sta, level=0, time=time1, dtime=dtime,
                                                           data_name=data_name)
    fo_sta_on_one_time_and_onedtime_all_dict[i] = fo_sta


def get_dim_type_info(para_dim_type, dim_type_sta_all_dict):
    if para_dim_type is not None:
        dim_type_num = len(para_dim_type)
        dim_type_sta1_list = []
        for i in range(dim_type_num):
            dim_type_sta1_list.append(None)
            path = para_dim_type[i]["path"]
            fix = True
            if path.find("YY") > 0:
                fix = False
            if path.find("MM") > 0:
                fix = False
            if path.find("DD") > 0:
                fix = False
            if path.find("HH") > 0:
                fix = False
            para_dim_type[i]["fix"] = fix

        # print(para_dim_type)
        for i in range(dim_type_num):
            dim_type_sta_all_dict[i] = None
        return dim_type_sta1_list, dim_type_num
    # fo_type_num ：预报数据模式个数


def get_time_set_in_group_set(para, time_name):
    if para["group_set"][time_name] != "fold":
        list_list = para["group_set"][time_name]["group"]
        list1 = []
        for list0 in list_list:
            list1.extend(list0)
        time_list = list(set(list1))
    else:
        if time_name == 'hour':
            time_list = np.arange(24).tolist()
        else:
            time_list = np.arange(1, 13).tolist()

    return time_list