import json
from urllib import request as urllib2
from django.conf import settings
from collections import OrderedDict
from itertools import chain
from collections import Counter
from master.models import SURVEYTYPE_CHOICES, Survey
from django.shortcuts import get_object_or_404
from graphs.models import *
import itertools
from graphs.sync_avni_data import *

def survey_mapping(survey_type):
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            city_id = args[0]
            try:
                survey = Survey.objects.filter(city__id=city_id, survey_type=survey_type)
            except:
                survey = None
            kwargs['kobo_survey'] = ''
            if survey:
                kwargs['kobo_survey'] =  survey[0].kobotool_survey_id
            return function(*args, **kwargs)
        return wrapper
    return real_decorator


def get_household_analysis_data_for_UP(question_fields):
    path = ""
    output = {}
    with open(path) as datafile:
        household_data = json.load(datafile)
    for household_obj in household_data:
        household_no = household_obj['household_number'].lstrip('0')
        rhs_data = household_obj['rhs_data']
        if 'Functioning of the structure' in rhs_data and rhs_data['Functioning of the structure'] == 'Shop':
            rhs_data['Type_of_structure_occupancy'] = 'Shop'
        # print(question_fields)
        for ques in question_fields:
            if ques in rhs_data and rhs_data[ques] and (rhs_data[ques] == rhs_data[ques]) and household_no not in ['10310', '10311', '10312']:
                ques_ans = rhs_data[ques]
                if ques == 'group_oi8ts04/Current_place_of_defecation':
                        if ques_ans == 'Yes':
                            ques_ans = 'Toilet Available'
                        else:
                            ques_ans = 'No Toilet'

                if ques not in output:
                    output[ques] = {ques_ans:[str(household_no), ]}
                else:
                    if ques_ans not in output[ques]:
                        output[ques][ques_ans] = [str(household_no), ]
                    else:
                        output[ques][ques_ans].append(household_no)
    return output



#@survey_mapping(SURVEYTYPE_CHOICES[1][0])
def get_household_analysis_data(city, slum_code, question_fields, kobo_survey=''):
    '''Gets the kobotoolbox RHS data for selected questions
    '''
    output = {}
    slum = get_object_or_404(Slum, id=slum_code)
    hide_houdehold_data = [1303807, 1303809, 1303815, 1302608, 1445969, 1303816, 1302615, 1302656, 1302659, 1302664, 1302674, 1302690, 1302691, 1302693, 1302696, 1302697, 1302698, 1302700, 1302701, 1302702, 1302704, 1302706, 1302707, 1302708, 1302709, 1302710, 1302712, 1302716, 1302717, 1302718, 1302719, 1302720, 1302723, 1302724, 1302725, 1302727, 1302728, 1302731, 1302732, 1302733, 1302734, 1302735, 1302736, 1302737, 1302738, 1302739, 1302740, 1302742, 1302743, 1302744, 1302745, 1302747, 1302748, 1302749, 1302750, 1302751, 1302752, 1302757, 1302758, 1302759, 1302760, 1302761, 1302762, 1302763, 1302764, 1302765, 1302766, 1302771, 1302772, 1302773, 1302774, 1302775, 1302778, 1302779, 1302780, 1302781, 1302782, 1302783, 1302784, 1302785, 1302786, 1302787, 1302788, 1302789, 1302790, 1302791, 1302792, 1302793, 1302794, 1302905, 1302906, 1302908, 1302912, 1302913, 1302914, 1302917, 1302918, 1302925, 1302928, 1302930, 1302931, 1302932, 1302943, 1302945, 1302946, 1302947, 1302948, 1302951, 1302952, 1302954, 1302958, 1302959, 1302960, 1302961, 1302968, 1302975, 1302979, 1302980, 1302981, 1302982, 1302983, 1302986, 1302989, 1302992, 1302995, 1302998, 1302999, 1303004, 1303005, 1303006, 1303008, 1303010, 1303013, 1303016, 1303019, 1303023, 1451254, 1303037, 1303039, 1303066, 1303067, 1303072, 1303076, 1303078, 1451266, 1451273, 1448770, 1448771, 1448774, 1448775, 1448776, 1448777, 1448780, 1448781, 1448782, 1448784, 1448785, 1448787, 1448788, 1448790, 1448791, 1448792, 1448793, 1448803, 1448805, 1448806, 1448807, 1448810, 1448854, 1448867, 1448869, 1448875, 1448876, 1448878, 1450960, 1448917, 1448918, 1450977, 1450979, 1448936, 1450986, 1448940, 1450988, 1451000, 1451001, 1451002, 1451003, 1451004, 1451005, 1451006, 1451007, 1448958, 1305605, 1305607, 1305608, 1451023, 1451024, 1451027, 1451028, 1451029, 1451030, 1305620, 1451041, 1305634, 1451042, 1451044, 1451043, 1451046, 1451047, 1451048, 1451045, 1451050, 1451051, 1469484, 1305645, 1451054, 1451055, 1451056, 1451057, 1451058, 1451059, 1451060, 1305653, 1451061, 1305655, 1451062, 1305680, 1305681, 1305682, 1305684, 1305685, 1305692, 1305694, 1305695, 1305696, 1305697, 1305699, 1305700, 1305701, 1305705, 1305706, 1305707, 1305708, 1305709, 1305711, 1305712, 1305713, 1305716, 1305717, 1305718, 1305723, 1305728, 1305729, 1305730, 1305751, 1305754, 1305756, 1305757, 1305759, 1305776, 1305777, 1305790, 1305791, 1303749, 1303750, 1303754, 1303756, 1303758, 1303762, 1303763, 1303764, 1303766, 1303768, 1303772, 1303773, 1303774, 1451231, 1451232, 1451233, 1451234, 1451235, 1451236, 1303780, 1451238, 1451239, 1451240, 1451241, 1303782, 1451237, 1303783, 1303784, 1451242, 1451246, 1303792, 1451249, 1451250, 1451251, 1451252, 1303797, 1451253, 1451255, 1451256, 1451257, 1303801, 1303803, 1303804, 1451261, 1451262, 1451263, 1451264, 1451265, 1303810, 1451267, 1451268, 1303811, 1451269, 1303813, 1303814, 1451270, 1451271, 1451272, 1303818, 1451274, 1451276, 1451277, 1451278, 1303825, 1303819, 1303824, 1451275, 1303821, 1451279, 1451280, 1303828, 1451289, 1451281, 1451288, 1451286, 1451287, 1451290, 1451291, 1451292, 1451293, 1451294, 1451296, 1451297, 1451298, 1451299, 1451300, 1451301, 1451302, 1451303, 1451305, 1451306, 1451307, 1451308, 1451309, 1451310, 1451311, 1451312, 1451313, 1451314, 1451315, 1451316, 1451317, 1451318, 1305907, 1305906, 1451324, 1305926, 1305942, 1447259, 1447260, 1447261, 1306027, 1306075, 1306120, 1306128, 1306135, 1445421, 1445422, 1445423, 1445424, 1445426, 1445440, 1445441, 1445446, 1445450, 1445451, 1451654, 1451680, 1451695, 1451696, 1451697, 1451698, 1451699, 1451701, 1451703, 1451704, 1451707, 1451718, 1435440, 1303775, 1303781, 1303785, 1303790, 1303795]
    household_data = HouseholdData.objects.filter(slum=slum).exclude(id__in = hide_houdehold_data)
    records = map(lambda x:x.rhs_data, household_data)
    records = filter(lambda x: x!=None, records)
    grouped_records = itertools.groupby(sorted(records, key=lambda x:int(x['Household_number'])), key=lambda x:int(x["Household_number"]))
    # For Covid Data
    covid_data = CovidData.objects.filter(slum = slum, age__gt = 17).exclude(household_number = 9999).values_list('household_number',flat = True)
    Toilet_data = list(ToiletConstruction.objects.filter(slum = slum, status = 6).values_list('household_number', flat = True))
    covid_hh = list(set(covid_data))
    cpod_status = ['SBM (Installment)','SBM (Contractor)','Toilet by SA (SBM)','Toilet by other NGO (SBM)','Own toilet','Toilet by other NGO','Toilet by SA']
    for household, list_record in grouped_records:
        record_sorted = list(list_record) #sorted(list(list_record), key=lambda x:x['_submission_time'], reverse=False)
        household_no = int(household)
        if len(record_sorted)>0:
            record = record_sorted[0]
        # Here we are updating vaccination status for the household.
        if record['Type_of_structure_occupancy'] != 'Shop':
            if household_no in covid_hh:
                cnt_mem = list(covid_data).count(household_no)
                # we use (__lte for lessthen equal to __lt for lessthen, __gte for graterthen equal to, __gt for graterthen)
                query_ = CovidData.objects.filter(household_number = household_no, slum = slum, take_first_dose = 'Yes', take_second_dose = 'Yes', age__gt = 17).values_list('household_number')
                query_1 = CovidData.objects.filter(household_number = household_no, slum = slum, take_first_dose = 'Yes', age__gt = 17).values_list('household_number')
                if query_ and query_.count() == cnt_mem:
                    record['vaccination_status'] = 'full_vaccinated'
                elif query_1 and query_1.count() > 0:
                    record['vaccination_status'] = 'partial_vaccinated'
                else:
                    record['vaccination_status'] = 'not_vaccinated'
            else:
                record['vaccination_status'] = 'not_surveyed'

        # Checking sbm and toilet by sa for filter.
        if 'group_oi8ts04/Current_place_of_defecation' in record and record['group_oi8ts04/Current_place_of_defecation'] in cpod_status[:4]:
            record['Final_status'] = 'SBM'
            record['group_oi8ts04/Current_place_of_defecation'] = 'Use CTB'
        if str(household_no) in Toilet_data:
            if 'group_oi8ts04/Current_place_of_defecation' in record and record['group_oi8ts04/Current_place_of_defecation'] in cpod_status:
                record['group_oi8ts04/Current_place_of_defecation'] = 'Use CTB'
            record['Final_status'] = 'Completed'

        # changing intrested status for hh where toilet present.
        if 'group_oi8ts04/Current_place_of_defecation' in record:
            if record['group_oi8ts04/Current_place_of_defecation'] in cpod_status or 'Final_status' in record:
                    if 'group_oi8ts04/Are_you_interested_in_an_indiv' in record:
                        del record['group_oi8ts04/Are_you_interested_in_an_indiv']
            elif record['group_oi8ts04/Current_place_of_defecation'] == 'Use CTB':
                record['remain_ctb'] = 'available' # Checking remining CTB's for POST SBM
            
            if 'group_oi8ts04/Are_you_interested_in_an_indiv' in record and record['group_oi8ts04/Are_you_interested_in_an_indiv'] == 'Yes':
                record['remain_intrested'] = 'Yes'   # Checking remining Interested for POST SBM
        
        '''question_fields is the different types of parameter of RHS Data.'''
        for field in question_fields:
            '''field present in rhs data'''
            if field != "" and field in record and record[field] == record[field]:
                '''RHS data is occupied in status or not.'''
                if record['Type_of_structure_occupancy'] != 'Occupied house':
                    if field == 'Type_of_structure_occupancy': # here we will check only for occupancy field.
                        data = record[field]
                        if field not in output:
                            output[field] = {data:[str(household_no), ]}
                        else:
                            if data not in output[field]:
                                output[field][data] = [str(household_no), ]
                            else:
                                output[field][data].append(str(household_no))
                else:
                    data = record[field]
                    for val in data if type(data)==list else data.split(','):
                        if field not in output:
                            output[field] = {}
                        if val not in output[field]:
                            output[field][val]=[]
                        if household_no not in output[field][val]:
                            output[field][val].append(str(household_no))
            elif record['Type_of_structure_occupancy'] == 'Occupied house' and field in ['group_el9cl08/Type_of_water_connection', 'group_el9cl08/Facility_of_solid_waste_collection', 'group_oi8ts04/Current_place_of_defecation']:
                ''' Checking encounter data not available if hh status is occupied.'''
                if field in output:
                    if  'data_not_available' in output[field]:
                        output[field]['data_not_available'].append(str(household_no))
                    else:
                        output[field]['data_not_available'] = [str(household_no), ]
                else:
                    output[field] = {'data_not_available' : [str(household_no), ]}
    return output

def format_data(rhs_data, toilet_by_sa = False):
    ''' Create RHS Data to show on spatial data'''
    new_rhs = {}
    remove_list = ['Name_s_of_the_surveyor_s', 'Date_of_survey', '_xform_id_string', 'meta/instanceID', 'end', 'start',
    'Enter_household_number_again','_geolocation', 'meta/deprecatedID', '_uuid', '_submitted_by', 'admin_ward', '_status',
    'formhub/uuid', '__version__','_submission_time', '_id', '_notes', '_bamboo_dataset_id', '_tags', 'slum_name', '_attachments',
    'OD1', 'C1', 'C2', 'C3','Household_number', '_validation_status']

    seq = {'group_el9cl08/Number_of_household_members': 'Number of household members',
        'group_oi8ts04/Have_you_applied_for_individua': 'Have you applied for an individual toilet under SBM?',
        'Type_of_structure_occupancy': 'Type of structure occupancy',
        'group_oi8ts04/Current_place_of_defecation': 'Current place of defecation',
        'group_el9cl08/Type_of_structure_of_the_house': 'Type of structure of the house',
        'group_oi8ts04/What_is_the_toilet_connected_to': 'What is the toilet connected to',
        'Household_number': 'Household number',
        'group_el9cl08/Type_of_water_connection': 'Type of water connection',
        'group_el9cl08/Facility_of_solid_waste_collection': 'Facility of solid waste collection',
        'group_el9cl08/Ownership_status_of_the_house': 'Ownership status of the house',
        'group_el9cl08/Does_any_household_m_n_skills_given_below': 'Does any household member have any of the construction skills given below?',
        'group_el9cl08/Enter_the_10_digit_mobile_number':'Mobile number',
        'group_el9cl08/House_area_in_sq_ft': 'House area in sq. ft.','group_og5bx85/Type_of_survey': 'Type of survey',
        'group_og5bx85/Full_name_of_the_head_of_the_household': 'Full name of the head of the household',
        'group_el9cl08/Do_you_have_any_girl_child_chi': 'Do you have any girl child/children under the age of 18?',
        'group_oi8ts04/Are_you_interested_in_an_indiv': 'Are you interested in an individual toilet?',
        'Plus code of the house' : 'Plus code of the house',
        "If individual water connection, type of water meter?":"If individual water connection, type of water meter?"
        }
    for i in remove_list:
        if i in rhs_data:
            rhs_data.pop(i)
    cpod_status = ['SBM (Installment)','SBM (Contractor)','Toilet by SA (SBM)','Toilet by other NGO (SBM)','Own toilet','Toilet by other NGO','Toilet by SA']

    for k, v in seq.items():
        try:
            
            if k == 'group_oi8ts04/Current_place_of_defecation':   # Changing cpod status and adding new cpod for toilet by sa households.
                if toilet_by_sa:
                    new_rhs[v] = 'Toilet By SA'
                    new_rhs['Before Home Toilet Place of defication'] = rhs_data[k]
                    if 'group_oi8ts04/Are_you_interested_in_an_indiv' in rhs_data:   # Removing household from intrested for toilet if household have toilet.
                        del rhs_data['group_oi8ts04/Are_you_interested_in_an_indiv']
                elif rhs_data[k] in cpod_status:
                    new_rhs['Before Home Toilet Place of defication'] = 'Use CTB'   #  If the hh has Toilet by sbm then cpod is Use CTB.
                    if 'group_oi8ts04/Are_you_interested_in_an_indiv' in rhs_data:
                        del rhs_data['group_oi8ts04/Are_you_interested_in_an_indiv']  # Removing household from intrested for toilet if household have toilet.
                    new_rhs[v] = rhs_data[k]
                else:
                    if k in rhs_data:
                        new_rhs[v] = rhs_data[k]
            else:
                if k in rhs_data:
                    new_rhs[v] = rhs_data[k]
            if k == 'Plus code of the house':
                new_rhs[v] =  (rhs_data[k] + " " + rhs_data["Plus Code Part"]) if "Plus Code Part" in rhs_data else rhs_data[k]
        except Exception as e:pass
    return new_rhs

@survey_mapping(SURVEYTYPE_CHOICES[1][0])
def get_kobo_RHS_list(city, slum, house_number, kobo_survey=''):
    """Method which fetches RHS data using the Kobo Toolbox API. Data contains question and answer decrypted. """
    output=OrderedDict()
    household_data = HouseholdData.objects.filter(slum=slum,household_number=house_number).order_by('submission_date')
    Toilet_data = list(ToiletConstruction.objects.filter(slum = slum, status = 6).values_list('household_number', flat = True))
    if len(household_data)>0:
        if str(int(house_number)) in Toilet_data:
            output = format_data(household_data[0].rhs_data, True)
        else:
            output = format_data(household_data[0].rhs_data)
    return output

def getPlusCodeDetails(slum, household):
    rhs_obj = HouseholdData.objects.filter(slum = slum, household_number = str(int(household)), rhs_data__isnull = False)
    if rhs_obj.exists():
        rhs_data = rhs_obj.values_list('rhs_data', flat = True)[0]
        if 'Plus code of the house' in rhs_data:
            if 'Plus Code Part' in rhs_data:
                pluscode = rhs_data['Plus code of the house'] + "-" + rhs_data['Plus Code Part']
                return pluscode
            return rhs_data['Plus code of the house']
    return None


@survey_mapping(SURVEYTYPE_CHOICES[0][0])
def get_kobo_RIM_detail(city, slum_code, kobo_survey=''):
    """Method to get RIM data from kobotoolbox using the API. Data contains question and answer decrypted.
    """
    output=OrderedDict()
    slum = Slum.objects.filter(shelter_slum_code = slum_code)
    submission = SlumData.objects.filter(slum_id = slum[0].id).values_list('rim_data', flat = True)[0]
    if len(submission) > 0:
        output = parse_RIM_data(submission)
    return output

def parse_RIM_data(submission):
    """
    |||||||||| --------- Method For View Tabuler data tab in spatial GIS Dashboard ---------- ||||||||||
    parse RIM data function used in get_kobo_RIM_detail(function above)
    :param submission: 
    :param form_data: 
    :return: 
    
    """
    match_keys = {'Drainage': {'coverage_of_drains_across_the': 'Coverage of drains across the settlement',
                    'diameter_of_ulb_sewer_line_acr': 'Diameter of ULB sewer line across settlement',
                    'do_the_drains_get_blocked': 'Do the drains get blocked',
                    'is_the_drainage_gradient_adequ': 'Is the drainage gradient adequate',
                    'presence_of_drains_within_the': 'Presence of drains within the settlement'},
                    'General': {'Date_of_declaration': 'Date of declaration',
                    'admin_ward': 'admin_ward',
                    'approximate_area_of_the_settle': 'Approximate area of the settlement in square meters',
                    'development_plan_reservation': 'Development plan reservation',
                    'development_plan_reservation_t': 'Development plan reservation type',
                    'land_owner': 'Land owner',
                    'landmark': 'Landmark',
                    'legal_status': 'Legal Status',
                    'location': 'Location',
                    'number_of_huts_in_settlement': 'Number of huts in settlement (From RHS)',
                    'slum_name': 'slum_name',
                    'survey_sector_number': 'Survey/Sector Number',
                    'topography': 'Topography',
                    'year_established_according_to': 'Year established according to community'},
                    'Gutter': {'Presence_of_gutter': 'Presence of gutter',
                    'are_gutter_covered': 'Are gutter covered',
                    'coverage_of_gutter': 'Coverage of gutter',
                    'do_gutter_get_choked': 'Do gutter get choked',
                    'do_gutters_flood': 'Do gutters flood',
                    'is_gutter_gradient_adequate': 'Is gutter gradient adequate',
                    'type_of_gutter_within_the_sett': 'Type of gutter within the settlement'},
                    'Road': {'are_the_huts_below_or_above_th': 'Are the huts below or above the internal access road',
                    'average_width_of_arterial_road': 'Average width of arterial road',
                    'average_width_of_internal_road': 'Average width of internal roads',
                    'coverage_of_pucca_road_across': 'Coverage of pucca road across the settlement',
                    'finish_of_the_road': 'Finish of the road',
                    'is_the_settlement_below_or_abo': 'Is the settlement below or above the mainaccess road',
                    'point_of_vehicular_access_to_t': 'Point of vehicular access to the slum',
                    'presence_of_roads_within_the_s': 'Presence of roads within the settlement',
                    'type_of_roads_within_the_settl': 'Type of roads within the settlemet'},
                    'Toilet': {'Out_of_total_seats_o_of_pans_not_choked': 'Out of total seats, no of pans not choked',
                    'availability_of_electricity_in': 'Availability of electricity in toilet block for pumping water to overhead tank',
                    'availability_of_electricity_in_001': 'Availability of electricity in toilet block after dark',
                    'availability_of_water_in_the_t': 'Availability of water in the toilet block',
                    'cleanliness_of_the_ctb': 'Cleanliness of the CTB',
                    'condition_of_ctb_structure': 'Condition of CTB structure',
                    'condition_of_facility_for_chil': 'Condition of facility for children under 5 years of age',
                    'cost_of_pay_and_use_toilet_pe': 'Cost of pay and use toilet (per individual per use)',
                    'ctb_gender_usage': 'CTB gender usage',
                    'ctb_maintenance_provided_by': 'CTB maintenance provided by',
                    'distance_to_nearest_ulb_sewer': 'Distance to nearest ULB sewer line',
                    'does_the_ulb_ngo_communty_use': 'Does the ULB/NGO/Community use cleaning agents to clean the CTB?',
                    'facility_in_the_toilet_block_f': 'Facility in the toilet block for children under 5 years of age',
                    'fee_for_use_of_ctb_per_family': 'Fee for use of CTB (per family per month)',
                    'frequency_of_ctb_cleaning_by_U': 'Frequency of CTB cleaning by ULB/NGO/Community',
                    'is_the_CTB_in_use': 'Is the CTB in use',
                    'is_the_ctb_available_at_night': 'Is the CTB available at night',
                    'is_there_a_caretaker_for_the_C': 'Is there a caretaker for the CTB?',
                    'litres_of_water_used_by_commun': 'Litres of water used by community members (per one flush)',
                    'number_of_mixed_seats_allotted': 'Number of MIXED seats allotted but not in use',
                    'number_of_seats_allotted_to_me': 'Number of seats allotted to men',
                    'number_of_seats_allotted_to_me_001': 'Number of seats allotted to men but not in use',
                    'number_of_seats_allotted_to_wo': 'Number of seats allotted to women',
                    'number_of_seats_allotted_to_wo_001': 'Number of seats allotted to women but not in use',
                    'out_of_total_seats_no_of_doors_in_good_condition': 'Out of total seats no of doors in good condition',
                    'out_of_total_seats_no_of_pans_in_good_condition': 'Out of total seats no of pans in good condition',
                    'out_of_total_seats_no_of_seats_where_electricity_is_available': 'Out of total seats no of seats where electricity is available',
                    'out_of_total_seats_no_of_seats_where_tiles_on_floor_are_in_good_condition': 'Out of total seats no of seats where tiles on floor are in good condition',
                    'out_of_total_seats_no_of_seats_where_tiles_on_wall_are_in_good_condition': 'Out of total seats no of seats where tiles on wall are in good condition',
                    'sewage_disposal_system': 'Sewage disposal system',
                    'the_reason_for_men_not_using_t': 'The reason for men not using the seats',
                    'the_reason_for_the_mixed_seats': 'The Reason for the MIXED seats not in Use',
                    'the_reason_for_women_not_using': 'The reason for women not using the seats',
                    'total_number_of_mixed_seats_al': 'Total number of MIXED seats allotted',
                    'type_of_water_supply_in_ctb': 'Type of water supply in CTB', "ctb name" :  "ctb_name"},
                    'Waste': {'coverage_of_waste_collection_a_001': 'Coverage of door to door  waste collection',
                    'coverage_of_waste_collection_a_002': 'Coverage of waste collection by ULB ghantagadi',
                    'coverage_of_waste_collection_a_003': 'Coverage of waste collection by ULB van',
                    'do_the_member_of_community_dep': 'Do the member of community deposite waste in the drains',
                    'facility_of_waste_collection': 'Facility of waste collection',
                    'frequency_of_waste_collection_': 'Frequency of ULB van',
                    'frequency_of_waste_collection_001': 'Frequency of ULB ghantagadi',
                    'frequency_of_waste_collection__001': 'Frequency of cleaning garbage bin',
                    'frequency_of_waste_collection__002': 'Frequency of door to door waste collection',
                    'total_number_of_waste_containe': 'Total number of waste containers',
                    'where_are_the_communty_open_du': 'Where are the communty open dump sites'},
                    'Water': {'Total_number_of_standposts_NOT': 'Total number of standposts NOT in use',
                    'Total_number_of_standposts_in_': 'Total number of standposts in use',
                    'alternative_source_of_water': 'Alternative source of water',
                    'availability_of_water': 'Availability of water',
                    'coverage_of_wateracross_settle': 'Coverage of wateracross settlement',
                    'pressure_of_water_in_the_syste': 'Pressure of water in the system',
                    'quality_of_water_in_the_system': 'Quality of water in the system',
                    'total_number_of_handpumps_in_u': 'Total number of handpumps in use',
                    'total_number_of_handpumps_in_u_001': 'Total number of handpumps NOT in use',
                    'total_number_of_taps_in_use_n': 'Total number of taps in use',
                    'total_number_of_taps_in_use_n_001': 'Total number of taps NOT in use'}}
    output = OrderedDict()
    
    '''We Are iterating on the each section of the RIM data'''
    for key, value in submission.items():
        data = OrderedDict()
        if key != "Toilet":    # here we are iterating on all the non repetative section.
            match_keys_dict = match_keys[key]   # here we are matching the section key to actual name of the question.
            for key1, value1 in value.items():
                if key1 in match_keys_dict:
                    data[match_keys_dict[key1]] = value1
            output[key] = data
        else:
            match_keys_dict = match_keys[key]   # here we are iterating repetative section Toilet section
            cnt = 1
            output[key] = []
            for i in value:
                data1 = OrderedDict()
                for key1, value1 in i.items():
                    if key1 in match_keys_dict:
                        data1[match_keys_dict[key1]] = value1   # here we are matching the section key to actual name of the question.
                output[key].append(data1)

    return output

@survey_mapping(SURVEYTYPE_CHOICES[0][0])
def get_kobo_RIM_report_detail(city, slum_code, kobo_survey=''):
    """Method to get RIM data from kobotoolbox using the API. Data contain only answers decrypted.
    """
    output=OrderedDict()
    RIM_TOILET="group_te3dx03"
    slum = Slum.objects.filter(shelter_slum_code = slum_code)
    data = SlumData.objects.filter(slum_id = slum[0].id).values_list('rim_data', flat = True)[0]

    # Useful Functions ...
    def data_processing(data):
        keys = list(data.keys())
        d = {}
        for i in keys:
            d[i] = data[i]
        return data

    def dict_to_str(data_dict):
        try:
            result_str = ""
            if len(data_dict.keys())>1:
                data_dict_keys = list(data_dict.keys())
                for key in data_dict_keys:
                    result_str += "," + key + "(" +str(data_dict[key]) + ")"
            elif len(data_dict.keys()) == 0:
                return result_str
            else:
                data_dict_key = list(data_dict.keys())[0]
                result_str += "," + data_dict_key + "(" +str(data_dict[data_dict_key]) + ")"
            return result_str
        except Exception as e:
            print(e)
    
    # // 'General Information'
    general_info = data['General']
    output.update(data_processing(general_info))
    # //'Toilet Information'
    if 'Toilet' in data:
        toilet_info = data['Toilet']
        output['number_of_community_toilet_blo'] = len(toilet_info)
        seats_f_man = 0
        seats_f_woman = 0
        seats_f_mix = 0
        ctb_maintenance_provider = {}
        ctb_structure_condition = {}
        ctb_cleanliness_condition = {}
        ctb_for_under_5 = {}
        ctb_sewage_disposal_system = {}
        water_supply_condition = []
        
        for i in toilet_info:
            if 'is_the_CTB_in_use' in i and i['is_the_CTB_in_use'] == 'Yes':
                if 'number_of_seats_allotted_to_wo' in i:
                    seats_f_woman += int(i['number_of_seats_allotted_to_wo'])
                if 'total_number_of_mixed_seats_al' in i:
                    seats_f_mix += int(i['total_number_of_mixed_seats_al'])
                if 'number_of_seats_allotted_to_me' in i:
                    seats_f_man += int(i['number_of_seats_allotted_to_me'])
                if i['ctb_maintenance_provided_by'] in ctb_maintenance_provider:
                    ctb_maintenance_provider[i['ctb_maintenance_provided_by']] += 1
                else:
                    ctb_maintenance_provider[i['ctb_maintenance_provided_by']] = 1

                if i['condition_of_ctb_structure'] in ctb_structure_condition:
                    ctb_structure_condition[i['condition_of_ctb_structure']] += 1
                else:
                    ctb_structure_condition[i['condition_of_ctb_structure']] = 1
                
                if i['cleanliness_of_the_ctb'] in ctb_cleanliness_condition:
                    ctb_cleanliness_condition[i['cleanliness_of_the_ctb']] += 1
                else:
                    ctb_cleanliness_condition[i['cleanliness_of_the_ctb']] = 1

                if i['facility_in_the_toilet_block_f'] in ctb_for_under_5:
                    ctb_for_under_5[i['facility_in_the_toilet_block_f']] += 1
                else:
                    ctb_for_under_5[i['facility_in_the_toilet_block_f']] = 1

                if i['sewage_disposal_system'] in ctb_sewage_disposal_system:
                    ctb_sewage_disposal_system[i['sewage_disposal_system']] += 1
                else:
                    ctb_sewage_disposal_system[i['sewage_disposal_system']] = 1

                water_supply_condition.extend(i['type_of_water_supply_in_ctb'].split(","))
        
            output['number_of_seats_allotted_to_wo'] = seats_f_woman
            output['total_number_of_mixed_seats_al'] = seats_f_mix
            output['number_of_seats_allotted_to_me'] = seats_f_man

            water_supply_condition_dict = {i: water_supply_condition.count(i) for i in water_supply_condition}

            dict_to_str_keys = {'ctb_maintenance_provided_by':ctb_maintenance_provider, 'condition_of_ctb_structure':ctb_structure_condition, 
                                'cleanliness_of_the_ctb':ctb_cleanliness_condition, 'type_of_water_supply_in_ctb':water_supply_condition_dict, 'facility_in_the_toilet_block_f':ctb_for_under_5, 'sewage_disposal_system':ctb_sewage_disposal_system}
            for key in dict_to_str_keys.keys():
                if len(dict_to_str(dict_to_str_keys[key])) > 1:
                    output[key] = dict_to_str(dict_to_str_keys[key])[1:]
                else:
                    output[key] = ""
    else:
        output.update({'number_of_community_toilet_blo' : 0})
        output['number_of_seats_allotted_to_wo'] = output['total_number_of_mixed_seats_al'] = output['number_of_seats_allotted_to_me'] = 0

    # //Waste Management Information
    waste_info = data['Waste']
    output.update(data_processing(waste_info))
    # //Water Information
    water_info = data['Water']
    output.update(data_processing(water_info))
    # //Drainage Information
    drainage_info = data['Drainage']
    output.update(data_processing(drainage_info))
    # //Roads &amp; Access Information
    road_info = data['Road']
    output.update(data_processing(road_info))
    # //Gutter Information
    gutter_info = data['Gutter']
    output.update(data_processing(gutter_info))

    return output

def parse_RIM_answer(submission, data1):
    """
    parse RIM answer function used in get_kobo_RIM_report_detail(function above).
    :param submission:
    :param form_data:
    :return:
    """
    RIM_TOILET = "group_te3dx03"
    output = OrderedDict()
    for data in data1['children']:
        if data['type'] == "group":
            # Group wise get the entire list for questions
            sect_form_data = trav(data)
            # Find the list of keys available in the submission data
            toil_keys = [str(k) for k in submission[0].keys() if data['name'] in k]
            count = 0
            sub_key = []
            sub = []
            # Needed for toilet section which has repeat section
            for sub_k in toil_keys:
                if type(submission[0][sub_k]) == list:
                    count = len(submission[0][sub_k])
                    sub = submission[0][sub_k]
                    sub_key.extend(sum([list(k.keys()) for k in submission[0][sub_k]], []))
                else:
                    sub_key.append(sub_k)

            # Iterate through the list of questions for the group
            for sect_form in sect_form_data:
                output[sect_form['name']] = ""
                key = [x for x in sub_key if x.endswith(sect_form['name'])]
                # Check if the question has answer in the submission then only proceed further
                if len(key) > 0 and 'label' in sect_form:
                    if data['name'] != RIM_TOILET:
                        # Fetch the answer for select one/text/select multiple type question
                        ans = fetch_answer(sect_form, key, submission[0])
                        output[sect_form['name']] = ans
                    else:
                        # For toilet repeative section append the set of questions for all the CTB's if available
                        if key[0] in submission[0].keys():
                            ans = fetch_answer(sect_form, key, submission[0])
                            output[sect_form['name']] = ans
                        else:
                            arr_ans = []
                            for ind in range(count):
                                if key[0] in sub[ind].keys():
                                    ans = fetch_answer(sect_form, key, sub[ind])
                                    if ans:
                                        arr_ans.extend(ans.split(','))

                            ans = ""
                            if 'integer' in sect_form['type']:
                                ans = sum(map(int, arr_ans))
                            else:
                                c = Counter(arr_ans)
                                ans = ', '.join(["{}({})".format(x, y) for x, y in c.items()])
                            output[sect_form['name']] = ans
    return output

def parse_RIM_answer_with_toilet(submission, data1):
    """
    parse RIM answer function used in sync record in graphs sync data. This gives array of toilet and does not aggregates it.
    :param submission:
    :param form_data:
    :return:
    """
    RIM_ADMIN = "group_ws5ux48"
    output = OrderedDict()
    RIM_GENERAL = "group_zl6oo94"
    RIM_TOILET = "group_te3dx03"
    RIM_WATER = "group_zj8tc43"
    RIM_WASTE = "group_ks0wh10"
    RIM_DRAINAGE = "group_kk5gz02"
    RIM_GUTTER = "group_bv7hf31"
    RIM_ROAD = "group_xy9hz30"
    section = { RIM_GENERAL: "General", RIM_TOILET: "Toilet", RIM_WATER: "Water",
               RIM_WASTE: "Waste", RIM_DRAINAGE: "Drainage", RIM_GUTTER: "Gutter", RIM_ROAD: "Road"}

    output = OrderedDict()
    for data in data1['children']:
        if data['type'] == "group" and data['name'] in section.keys():
            # Group wise get the entire list for questions
            sect_form_data = trav(data)
            # Find the list of keys available in the submission data
            toil_keys = [str(k) for k in submission[0].keys() if data['name'] in k]
            count = 0
            sub_key = []
            sub = []
            # Needed for toilet section which has repeat section
            for sub_k in toil_keys:
                if type(submission[0][sub_k]) == list:
                    count = len(submission[0][sub_k])
                    sub = submission[0][sub_k]
                    sub_key.extend(sum([k.keys() for k in submission[0][sub_k]], []))
                else:
                    sub_key.append(sub_k)

            if data['name'] != RIM_TOILET:
                output[section[data['name']]] = OrderedDict()
            else:
                output[section[data['name']]] = []
                [output[section[data['name']]].append(OrderedDict()) for i in range(count)]

            # Iterate through the list of questions for the group
            for sect_form in sect_form_data:
                key = [x for x in sub_key if x.endswith(sect_form['name'])]
                # Check if the question has answer in the submission then only proceed further
                if len(key) > 0 and 'label' in sect_form:
                    if data['name'] != RIM_TOILET:
                        # Fetch the answer for select one/text/select multiple type question
                        ans = fetch_answer(sect_form, key, submission[0])
                        output[section[data['name']]][sect_form['name']]  = ans
                    else:
                        for ind in range(count):
                            #output[data['name']][ind][sect_form['label']] = ""
                            if key[0] in sub[ind].keys():
                                ans = fetch_answer(sect_form, key, sub[ind])
                                output[section[data['name']]][ind][sect_form['name']] = ans
    return output


@survey_mapping(SURVEYTYPE_CHOICES[3][0])
def get_kobo_FF_report_detail(city, slum_code,house_number, kobo_survey=''):
    """Method which fetches family factsheet data from kobotoolbox using the API's. Data contain only answers decrypted."""
    output=OrderedDict()
    if kobo_survey:
        householdData = HouseholdData.objects.filter(slum__shelter_slum_code = slum_code, household_number = str(house_number)).exclude(ff_data=None)
        if len(householdData) > 0 and householdData[0].ff_data:
            output = householdData[0].ff_data
            a = avni_sync()
            for key in list(output):
                split_key = key.split('/')
                if len(split_key) > 1:
                    output[split_key[-1:][0]] = output[key]
                    output.pop(key)
            if "_attachments" in output and len(output['_attachments']) != 0:
                PATH = 'https://app.shelter-associates.org/media/shelter/attachments/' + "/".join(output['_attachments'][0]["filename"].split('/')[2:-1])
                for photo in output["_attachments"]:
                    if 'Toilet_Photo' in output and output["Toilet_Photo"] in photo["filename"]:
                        output["Toilet_Photo"] = PATH +"/" + output["Toilet_Photo"]
                    if 'Family_Photo' in output and output["Family_Photo"] in photo["filename"]:
                        output["Family_Photo"] = PATH + "/" + output["Family_Photo"]
            else:
                if 'Toilet_Photo' in output :
                    toilet_image_url = a.get_image(output['Toilet_Photo'])
                    output["Toilet_Photo"] = toilet_image_url
                if 'Family_Photo' in output :
                    family_image_url = a.get_image(output['Family_Photo'])
                    output["Family_Photo"] = family_image_url
    return output

@survey_mapping(SURVEYTYPE_CHOICES[3][0])
def get_kobo_FF_report_detail1(city, slum_code,house_number, kobo_survey=''):
    """Method which fetches family factsheet data from kobotoolbox using the API's. Data contain only answers decrypted."""
    output=OrderedDict()
    if kobo_survey:
        try:
            url = settings.KOBOCAT_FORM_URL+'data/'+kobo_survey+'?format=json&query={"group_vq77l17/slum_name":"'+slum_code+'","group_vq77l17/Household_number":{"$in":["'+house_number+'","'+('000'+house_number)[-4:]+'"]}}'
        except Exception as e:
            print(e)

        req = urllib2.Request(url)
        req.add_header('Authorization', settings.KOBOCAT_TOKEN)
        resp = urllib2.urlopen(req)
        content = resp.read()
        submission = json.loads(content)

        url1 = settings.KOBOCAT_FORM_URL+'forms/'+kobo_survey+'/form.json'
        req1 = urllib2.Request(url1)
        req1.add_header('Authorization', settings.KOBOCAT_TOKEN)
        resp1 = urllib2.urlopen(req1)
        content1 = resp1.read()
        data1 = json.loads(content1)

        output = OrderedDict()
        if len(submission) > 0:
            for data in data1['children']:
                if data['type'] == "group" or data['type'] == "photo" or data['type'] == "text":
                    sect_form_data = trav(data)
                    sub_key = [ str(k) for k in submission[0].keys() if data['name'] in k] + ['_attachments']
                    for sect_form in sect_form_data:
                        output[sect_form['name']] = ""
                        key = [x for x in sub_key if x.endswith(sect_form['name'])]
                        if len(key)>0 and 'name' in sect_form:
                            ans = fetch_answer(sect_form, key, submission[0])
                            output[sect_form['name']]  = ans

    return output

def fetch_answer(sect_form, key, submission):
    #Fetch answer and convert it to label
    val = ""
    if 'select' in sect_form['type'] and type(key[0]) != list and 'children' in sect_form:
        options = dict((str(opt['name']), str(opt['label'])) for opt in sect_form['children'])
        sub_option = submission[key[0]].split(' ')
        val = []
        if len(sub_option) > 0:
            for sub in sub_option:
                if sub in options:
                    val.append(str(options[sub]))
        val = ', '.join(val)
    elif 'photo' in sect_form['type']:
        photos = submission['_attachments']
        val = [photo['download_url'] for photo in photos if submission[key[0]] in photo['filename']]
        if val and len(val)>0:
            val = val[0]
    else:
        val = submission[key[0]]
    return val

def trav(node):
    #Traverse uptill the child node and add to list
    if 'type' in node and node['type'] == "group" or node['type'] == "repeat":
        return list(chain.from_iterable([trav(child) for child in node['children']]))
    else:
        return [node]

def dictdata(data):
    #convert childrens to dictionary for parsing
    data['children'] = dict((str(topic['name']), topic) for topic in data['children'])

    for k,v in data['children'].items():
        if 'children' in v:
            if isinstance(v['children'], list):
                v = dictdata(v)
    return data
