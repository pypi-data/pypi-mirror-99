from decimal import Decimal

from django.core.validators import validate_comma_separated_integer_list
from django.utils.translation import gettext_lazy as _, pgettext_lazy
from django_countries.serializer_fields import CountryField
from internationalflavor.iban import IBANValidator
from internationalflavor.vat_number import VATNumberValidator
from model_utils.choices import Choices
from rest_framework import serializers

from easys_ordermanager.fields import PhoneNumberField
from easys_ordermanager.validators import comma_separated_period_validatior, HexColorValidator, \
    DomainNameValidator

PAYMENT_METHOD_TRANSFER = 1
PAYMENT_METHOD_CHARGE = 2
PAYMENT_METHOD_CHOICES = Choices(
    (PAYMENT_METHOD_TRANSFER, 'transfer', _('Transfer')),
    (PAYMENT_METHOD_CHARGE, 'charge', _('Charge')),
)

TITLE_UNKNOWN = 0
TITLE_MR = 1
TITLE_MRS = 2
TITLE_MR_DR = 3
TITLE_MRS_DR = 4
TITLE_MR_PROF = 5
TITLE_MRS_PROF = 6
TITLE_CHOICES = Choices(
    (TITLE_UNKNOWN, 'unknown', _('Unknown')),
    (TITLE_MR, 'mr', _('Mr.')),
    (TITLE_MRS, 'mrs', _('Mrs.')),
    (TITLE_MR_DR, 'mr_dr', _('Mr. Dr.')),
    (TITLE_MRS_DR, 'mrs_dr', _('Mrs. Dr.')),
    (TITLE_MR_PROF, 'mr_prof', _('Mr. Prof.')),
    (TITLE_MRS_PROF, 'mrs_prof', _('Mrs. Prof.')),
)

NEW_WEBSITE = 1
CUSTOMER_WEBSITE = 2
NEW_LANDINGPAGE = 3
LANDING_PAGE_CHOICES = Choices(
    (NEW_WEBSITE, 'new', _('New website')),
    (CUSTOMER_WEBSITE, 'customer', _('Customer website')),
)

GOOGLE_ADS_LANDING_PAGE_CHOICES = Choices(
    (NEW_WEBSITE, 'new', _('New website')),
    (NEW_LANDINGPAGE, 'new_lp', _('New landingpage')),
    (CUSTOMER_WEBSITE, 'customer', _('Customer website')),
)

PRODUCT_LEVEL_BASIC = 1
PRODUCT_LEVEL_PREMIUM = 2
PRODUCT_LEVEL_PROFESSIONAL = 3
PRODUCT_LEVEL_CHOICES = Choices(
    (PRODUCT_LEVEL_BASIC, 'basic', _('Basic')),
    (PRODUCT_LEVEL_PREMIUM, 'premium', _('Premium')),
    (PRODUCT_LEVEL_PROFESSIONAL, 'professional', _('Professional')),
)

PRODUCT_TYPE_GOOGLE_ADS = 1
PRODUCT_TYPE_DISPLAY = 2
PRODUCT_TYPE_IN_APP = 3
PRODUCT_TYPE_SEO = 4
PRODUCT_TYPE_LISTING = 5
PRODUCT_TYPE_WEBSITE = 6
PRODUCT_TYPE_FACEBOOK = 7
PRODUCT_TYPE_CUSTOMER_WEBSITE = 8
PRODUCT_TYPE_EMAIL = 9
PRODUCT_TYPE_CONVERSION_TRACKING = 10
PRODUCT_TYPE_LANDINGPAGE = 11
PRODUCT_TYPE_TONLINE = 12
PRODUCT_TYPE_CHOICES = Choices(
    (PRODUCT_TYPE_GOOGLE_ADS, 'google_ads', _('Google Ads')),
    (PRODUCT_TYPE_DISPLAY, 'display', _('Display')),
    (PRODUCT_TYPE_IN_APP, 'in_app', _('In-App advertisement')),
    (PRODUCT_TYPE_SEO, 'seo', _('SEO')),
    (PRODUCT_TYPE_LISTING, 'listing', _('Listing')),
    (PRODUCT_TYPE_WEBSITE, 'website', _('Website')),
    (PRODUCT_TYPE_LANDINGPAGE, 'landingpage', _('Landingpage')),
    (PRODUCT_TYPE_FACEBOOK, 'facebook', _('Facebook')),
    (PRODUCT_TYPE_CUSTOMER_WEBSITE, 'customer_website', _('Customer website')),
    (PRODUCT_TYPE_EMAIL, 'email', _('Email')),
    (PRODUCT_TYPE_CONVERSION_TRACKING, 'conversion_tracking', _('Conversion tracking')),
    (PRODUCT_TYPE_TONLINE, 'tonline', _('T-Online')),
)

PRODUCT_PAYMENT_CYCLE_1 = 1
PRODUCT_PAYMENT_CYCLE_3 = 3
PRODUCT_PAYMENT_CYCLE_6 = 6
PRODUCT_PAYMENT_CYCLE_12 = 12
PRODUCT_PAYMENT_CYCLE_CHOICES = Choices(
    (PRODUCT_PAYMENT_CYCLE_1, 'one_month', _('Monthly')),
    (PRODUCT_PAYMENT_CYCLE_3, 'three_months', _('Quarterly')),
    (PRODUCT_PAYMENT_CYCLE_6, 'six_months', _('Biyearly')),
    (PRODUCT_PAYMENT_CYCLE_12, 'twelve_months', _('Yearly')),
)

PRODUCT_TYPE_ORDER_ATTRIBUTES_MAPPING = {
    PRODUCT_TYPE_GOOGLE_ADS: {'detail_google_ads_basic', 'detail_google_ads_premium'},
    PRODUCT_TYPE_DISPLAY: {'detail_display_basic', 'detail_display_premium'},
    PRODUCT_TYPE_FACEBOOK: {'detail_facebook'},
    PRODUCT_TYPE_IN_APP: {'detail_inapp'},
    PRODUCT_TYPE_LISTING: {'detail_listing'},
    PRODUCT_TYPE_SEO: {'detail_seo'},
    PRODUCT_TYPE_WEBSITE: {'detail_website'},
    PRODUCT_TYPE_LANDINGPAGE: {'detail_landingpage'},
    PRODUCT_TYPE_CUSTOMER_WEBSITE: {'detail_customer_website'},
    PRODUCT_TYPE_EMAIL: {'detail_email'},
}

CREATIVE_OPTION_CUSTOMER = 1
CREATIVE_OPTION_CREATE_STATIC = 2
CREATIVE_OPTION_CREATE_ANIMATED = 3
CREATIVE_OPTION_CHOICES = Choices(
    (CREATIVE_OPTION_CUSTOMER, 'customer', _('Customer provided')),
    (CREATIVE_OPTION_CREATE_STATIC, 'create_static', _('Create static')),
    (CREATIVE_OPTION_CREATE_ANIMATED, 'create_animated', _('Create animated')),
)

BOOKING_TYPE_FIXED = 1
BOOKING_TYPE_CONTINUOUS = 2
BOOKING_TYPE_CHOICES = Choices(
    (BOOKING_TYPE_FIXED, 'fixed', _('Fixed runtime ad')),
    (BOOKING_TYPE_CONTINUOUS, 'continuous', _('Continuous ad')),
)

LOGO_CREATION_NEW = 1
LOGO_CREATION_EXISTING = 2
LOGO_CREATION_NONE = 3
LOGO_CREATION_CHOICES = Choices(
    (LOGO_CREATION_NEW, 'new', _('Create new logo')),
    (LOGO_CREATION_EXISTING, 'existing', _('Use existing logo')),
    (LOGO_CREATION_NONE, 'none', _('No logo at all, text only')),
)

LOGO_TYPE_DESIGN_MARK = 1
LOGO_TYPE_WORD_MARK = 2
LOGO_TYPE_COMPOSITE_MARK = 3
LOGO_TYPE_CHOICES = Choices(
    (LOGO_TYPE_DESIGN_MARK, 'design', _('Design mark')),
    (LOGO_TYPE_WORD_MARK, 'word', _('Word mark')),
    (LOGO_TYPE_COMPOSITE_MARK, 'composite', _('Composite mark')),
)

WEBSITE_DESIGN_PREFERENCE_MINIMALISTIC = 1
WEBSITE_DESIGN_PREFERENCE_BALANCED = 2
WEBSITE_DESIGN_PREFERENCE_EMBELLISHED = 3
WEBSITE_DESIGN_PREFERENCE_MINIMALISTIC_EMBELLISHED = Choices(
    (WEBSITE_DESIGN_PREFERENCE_MINIMALISTIC, _('Minimalistic')),
    (WEBSITE_DESIGN_PREFERENCE_BALANCED, _('Balanced minimalistic / embellished')),
    (WEBSITE_DESIGN_PREFERENCE_EMBELLISHED, _('Embellished')),
)

WEBSITE_DESIGN_PREFERENCE_MODERN = 1
WEBSITE_DESIGN_PREFERENCE_CLASSIC = 3
WEBSITE_DESIGN_PREFERENCE_MODERN_CLASSIC = Choices(
    (WEBSITE_DESIGN_PREFERENCE_MODERN, _('Modern')),
    (WEBSITE_DESIGN_PREFERENCE_BALANCED, _('Balanced modern / classic')),
    (WEBSITE_DESIGN_PREFERENCE_CLASSIC, _('Classic')),
)

WEBSITE_DESIGN_PREFERENCE_SIMPLE = 1
WEBSITE_DESIGN_PREFERENCE_STRIKING = 3
WEBSITE_DESIGN_PREFERENCE_SIMPLE_STRIKING = Choices(
    (WEBSITE_DESIGN_PREFERENCE_SIMPLE, _('Simple')),
    (WEBSITE_DESIGN_PREFERENCE_BALANCED, _('Balanced simple / striking')),
    (WEBSITE_DESIGN_PREFERENCE_STRIKING, _('Striking')),
)

WEBSITE_DESIGN_PREFERENCE_TEXT = 1
WEBSITE_DESIGN_PREFERENCE_PICTURE = 3
WEBSITE_DESIGN_PREFERENCE_TEXT_PICTURE = Choices(
    (WEBSITE_DESIGN_PREFERENCE_TEXT, _('Text-heavy')),
    (WEBSITE_DESIGN_PREFERENCE_BALANCED, _('Balanced text-heavy / picture-heavy')),
    (WEBSITE_DESIGN_PREFERENCE_PICTURE, _('Picture-heavy')),
)

DOMAIN_TYPE_NEW = 1
DOMAIN_TYPE_TRANSFER = 2
DOMAIN_TYPE_EXTERNAL = 3
DOMAIN_TYPE_CHOICES = Choices(
    (DOMAIN_TYPE_NEW, 'new', _('Register new one')),
    (DOMAIN_TYPE_TRANSFER, 'transfer', _('Transfer existing one')),
    (DOMAIN_TYPE_EXTERNAL, 'external', _('Use external one')),
)

OPENING_HOURS_WEEK_DAY_MONDAY = 1
OPENING_HOURS_WEEK_DAY_TUESDAY = 2
OPENING_HOURS_WEEK_DAY_WEDNESDAY = 3
OPENING_HOURS_WEEK_DAY_THURSDAY = 4
OPENING_HOURS_WEEK_DAY_FRIDAY = 5
OPENING_HOURS_WEEK_DAY_SATURDAY = 6
OPENING_HOURS_WEEK_DAY_SUNDAY = 7
OPENING_HOURS_WEEK_DAY_CHOICES = Choices(
    (OPENING_HOURS_WEEK_DAY_MONDAY, 'monday', _('Monday')),
    (OPENING_HOURS_WEEK_DAY_TUESDAY, 'tuesday', _('Tuesday')),
    (OPENING_HOURS_WEEK_DAY_WEDNESDAY, 'wednesday', _('Wednesday')),
    (OPENING_HOURS_WEEK_DAY_THURSDAY, 'thursday', _('Thursday')),
    (OPENING_HOURS_WEEK_DAY_FRIDAY, 'friday', _('Friday')),
    (OPENING_HOURS_WEEK_DAY_SATURDAY, 'saturday', _('Saturday')),
    (OPENING_HOURS_WEEK_DAY_SUNDAY, 'sunday', _('Sunday'))
)

OPENING_HOURS_MODE_OPEN = 1
OPENING_HOURS_MODE_OPEN_MORNING_AFTERNOON = 2
OPENING_HOURS_MODE_OPEN_24_HOURS = 3
OPENING_HOURS_MODE_CLOSED = 4
OPENING_HOURS_MODE_CHOICES = Choices(
    (OPENING_HOURS_MODE_OPEN, 'open', _('Open')),
    (OPENING_HOURS_MODE_OPEN_MORNING_AFTERNOON, 'open_morning_afternoon', _('Morning and afternoon')),
    (OPENING_HOURS_MODE_OPEN_24_HOURS, 'open_24_hours', _('Open 24 hours')),
    (OPENING_HOURS_MODE_CLOSED, 'closed', pgettext_lazy('opening hours', 'Closed'))
)

SEO_TEXT_STYLE_ADVERTISING = 1
SEO_TEXT_STYLE_FACTUAL = 2
SEO_TEXT_STYLE_CUSTOMER_RELATED = 3
SEO_TEXT_STYLE_CHOICES = Choices(
    (SEO_TEXT_STYLE_ADVERTISING, 'advertising', _('Advertising')),
    (SEO_TEXT_STYLE_FACTUAL, 'factual', _('Factual')),
    (SEO_TEXT_STYLE_CUSTOMER_RELATED, 'customer_related', _('Customer related')),
)

FACEBOOK_DETAILED_TARGETS_CATEGORY_EMPTY = 0
FACEBOOK_DETAILED_TARGETS_CATEGORY_JOB_TITLE = 1
FACEBOOK_DETAILED_TARGETS_CATEGORY_JOB_SECTOR = 2
FACEBOOK_DETAILED_TARGETS_CATEGORY_DEMOGRAPHY = 3
FACEBOOK_DETAILED_TARGETS_CATEGORY_INTERESTS = 4
FACEBOOK_DETAILED_TARGETS_CATEGORY_BEHAVIOUR = 5
FACEBOOK_DETAILED_TARGETS_CATEGORY_CHOICES = Choices(
    (FACEBOOK_DETAILED_TARGETS_CATEGORY_EMPTY, '', '-'),
    (FACEBOOK_DETAILED_TARGETS_CATEGORY_JOB_TITLE, 'job_title', _('Job title')),
    (FACEBOOK_DETAILED_TARGETS_CATEGORY_JOB_SECTOR, 'job_sector', _('Job sector')),
    (FACEBOOK_DETAILED_TARGETS_CATEGORY_DEMOGRAPHY, 'demography', _('Demography')),
    (FACEBOOK_DETAILED_TARGETS_CATEGORY_INTERESTS, 'interests', _('Interests')),
    (FACEBOOK_DETAILED_TARGETS_CATEGORY_BEHAVIOUR, 'behaviour', _('Behaviour')),
)

FACEBOOK_MARKETING_TARGET_WEBSITE_CLICKS = 1
FACEBOOK_MARKETING_TARGET_RETARGETING = 2
FACEBOOK_MARKETING_TARGET_EVENT_PROMOTION = 3
FACEBOOK_MARKETING_TARGET_BRAND = 4
FACEBOOK_MARKETING_TARGET_WIN_FANS = 5
FACEBOOK_MARKETING_TARGET_PROMOTE_ARTICLES = 6
FACEBOOK_MARKETING_TARGET_CHOICES = Choices(
    (FACEBOOK_MARKETING_TARGET_WEBSITE_CLICKS, 'website_clicks', _('Website clicks')),
    (FACEBOOK_MARKETING_TARGET_RETARGETING, 'retargeting_via_facebook', _('Retargeting via Facebook')),
    (FACEBOOK_MARKETING_TARGET_EVENT_PROMOTION, 'event_promotion', _('Event promotion')),
    (FACEBOOK_MARKETING_TARGET_BRAND, 'strengthen_the_brand', _('Strengthen the brand')),
    (FACEBOOK_MARKETING_TARGET_WIN_FANS, 'win_fans', _('Win fans')),
    (FACEBOOK_MARKETING_TARGET_PROMOTE_ARTICLES, 'promote_articles', _('Promote articles')),
)

FACEBOOK_AGE_13_17 = 1
FACEBOOK_AGE_18_24 = 2
FACEBOOK_AGE_25_34 = 3
FACEBOOK_AGE_35_44 = 4
FACEBOOK_AGE_45_54 = 5
FACEBOOK_AGE_55_PLUS = 6
FACEBOOK_AGE_CHOICES = Choices(
    (FACEBOOK_AGE_13_17, '13_17', _('13-17  years')),
    (FACEBOOK_AGE_18_24, '18_24', _('18-24  years')),
    (FACEBOOK_AGE_25_34, '25_34', _('25-34  years')),
    (FACEBOOK_AGE_35_44, '35_44', _('35-44  years')),
    (FACEBOOK_AGE_45_54, '45_54', _('45-54  years')),
    (FACEBOOK_AGE_55_PLUS, '55_plus', _('55 years or more')),
)

FACEBOOK_GENDER_INDIFFERENT = 1
FACEBOOK_GENDER_MALE = 2
FACEBOOK_GENDER_FEMALE = 3
FACEBOOK_GENDER_CHOICES = Choices(
    (FACEBOOK_GENDER_INDIFFERENT, 'indifferent', _('Indifferent')),
    (FACEBOOK_GENDER_MALE, 'male', _('Male')),
    (FACEBOOK_GENDER_FEMALE, 'female', _('Female')),
)

FACEBOOK_TEXT_SOURCE_WEBSITE = 1
FACEBOOK_TEXT_SOURCE_CUSTOMER = 2
FACEBOOK_TEXT_SOURCE_PROVIDER = 3
FACEBOOK_TEXT_SOURCE_CHOICES = Choices(
    (FACEBOOK_TEXT_SOURCE_WEBSITE, 'website', _('From website')),
    (FACEBOOK_TEXT_SOURCE_CUSTOMER, 'customer', _('Customer delivered')),
    (FACEBOOK_TEXT_SOURCE_PROVIDER, 'provider', _('Provider created')),
)

FACEBOOK_IMAGE_SOURCE_WEBSITE = 1
FACEBOOK_IMAGE_SOURCE_CUSTOMER = 2
FACEBOOK_IMAGE_SOURCE_PROVIDER = 3
FACEBOOK_IMAGE_SOURCE_CHOICES = Choices(
    (FACEBOOK_IMAGE_SOURCE_WEBSITE, 'website', _('From website')),
    (FACEBOOK_IMAGE_SOURCE_CUSTOMER, 'customer', _('Customer delivered')),
    (FACEBOOK_IMAGE_SOURCE_PROVIDER, 'provider', _('Provider created')),
)

INAPP_BANNERS_CREATOR_CUSTOMER = 1
INAPP_BANNERS_CREATOR_PROVIDER = 2
INAPP_BANNERS_CREATOR_CHOICES = Choices(
    (INAPP_BANNERS_CREATOR_CUSTOMER, 'customer', _('Creatives from the customer')),
    (INAPP_BANNERS_CREATOR_PROVIDER, 'provider', _('Creatives created by provider')),
)

INAPP_BANNER_TEMPLATE_ASK_CUSTOMER = 12
INAPP_BANNER_TEMPLATE_GALLERY_AD = 1
INAPP_BANNER_TEMPLATE_VIDEO_GALLERY_AD = 2
INAPP_BANNER_TEMPLATE_PANORAMA_AD = 3
INAPP_BANNER_TEMPLATE_ROLLEY_AD = 6
INAPP_BANNER_TEMPLATE_VIDEO_AD = 13
INAPP_BANNER_TEMPLATE_CUBE_AD = 4
INAPP_BANNER_TEMPLATE_CALL_AD = 9
INAPP_BANNER_TEMPLATE_CALENDAR_AD = 5
INAPP_BANNER_TEMPLATE_SOCIAL_SHARING_AD = 7
INAPP_BANNER_TEMPLATE_SCENE_SWITCH_AD = 10
INAPP_BANNER_TEMPLATE_FULLSCREEN_AD = 14
INAPP_BANNER_TEMPLATE_TITLE_AD = 8
INAPP_BANNER_TEMPLATE_HANDLER_AD = 11  # Not used any more
INAPP_BANNER_TEMPLATE_CHOICES = Choices(
    (INAPP_BANNER_TEMPLATE_ASK_CUSTOMER, 'ask_customer', _('Ask customer')),
    (INAPP_BANNER_TEMPLATE_GALLERY_AD, 'gallery_ad', _('Gallery Ad')),
    (INAPP_BANNER_TEMPLATE_VIDEO_GALLERY_AD, 'video_gallery_ad', _('Video gallery Ad')),
    (INAPP_BANNER_TEMPLATE_PANORAMA_AD, 'panorama_ad', _('Panorama Ad')),
    (INAPP_BANNER_TEMPLATE_ROLLEY_AD, 'rolley_ad', _('Rolley Ad')),
    (INAPP_BANNER_TEMPLATE_VIDEO_AD, 'video_ad', _('Video Ad')),
    (INAPP_BANNER_TEMPLATE_CUBE_AD, 'cube_ad', _('Cube Ad')),
    (INAPP_BANNER_TEMPLATE_CALL_AD, 'call_ad', _('Call Ad')),
    (INAPP_BANNER_TEMPLATE_CALENDAR_AD, 'calendar_ad', _('Calendar Ad')),
    (INAPP_BANNER_TEMPLATE_SOCIAL_SHARING_AD, 'social_sharing_ad', _('Social sharing Ad')),
    (INAPP_BANNER_TEMPLATE_SCENE_SWITCH_AD, 'scene_switch_ad', _('Scene switch Ad')),
    (INAPP_BANNER_TEMPLATE_FULLSCREEN_AD, 'fullscreen_ad', _('Fullscreen Ad')),
    (INAPP_BANNER_TEMPLATE_TITLE_AD, 'tile_ad', _('Tile Ad')),
    (INAPP_BANNER_TEMPLATE_HANDLER_AD, 'handler_ad', _('Handler Ad')),
)

DISPLAY_TYPE_WEB_MOBILE = 1
DISPLAY_TYPE_MOBILE_ONLY = 2
DISPLAY_TYPE_CHOICES = Choices(
    (DISPLAY_TYPE_WEB_MOBILE, 'web_and_mobile', _('Web and mobile display advertisement')),
    (DISPLAY_TYPE_MOBILE_ONLY, 'mobile_only', _('Mobile only display advertisement')),
)

DISPLAY_BANNER_IMAGE_SOURCE_WEBSITE = 0
DISPLAY_BANNER_IMAGE_SOURCE_CUSTOMER = 1
DISPLAY_BANNER_IMAGE_SOURCE_REGIOHELDEN = 2

DISPLAY_BANNER_IMAGE_SOURCE_CHOICES = Choices(
    (DISPLAY_BANNER_IMAGE_SOURCE_WEBSITE, 'website', _('From website')),
    (DISPLAY_BANNER_IMAGE_SOURCE_CUSTOMER, 'customer', _('From customer')),
    (DISPLAY_BANNER_IMAGE_SOURCE_REGIOHELDEN, 'regiohelden', _('Regiohelden photos')),
)

DISPLAY_BANNER_COLOR_SELECT_WEBSITE = 1
DISPLAY_BANNER_COLOR_SELECT_PICKER = 2
DISPLAY_BANNER_COLOR_SELECTION_CHOICES = Choices(
    (DISPLAY_BANNER_COLOR_SELECT_WEBSITE, 'website', _('Color from Logo/Website')),
    (DISPLAY_BANNER_COLOR_SELECT_PICKER, 'color_picker', _('Set color'))
)

DISPLAY_IMPRESSIONS_PER_MONTH_20 = 20000
DISPLAY_IMPRESSIONS_PER_MONTH_40 = 40000
DISPLAY_IMPRESSIONS_PER_MONTH_80 = 80000
DISPLAY_IMPRESSIONS_PER_MONTH_CHOICES = Choices(
    (DISPLAY_IMPRESSIONS_PER_MONTH_20, 'impressions_20', _('20.000 Impressions')),
    (DISPLAY_IMPRESSIONS_PER_MONTH_40, 'impressions_40', _('40.000 Impressions')),
    (DISPLAY_IMPRESSIONS_PER_MONTH_80, 'impressions_80', _('80.000 Impressions'))
)

DISPLAY_BASIC_CREATIVE_OPTION_CHOICES = Choices(
    (CREATIVE_OPTION_CUSTOMER, 'customer', _('Customer provided')),
    (CREATIVE_OPTION_CREATE_ANIMATED, 'create_animated', _('Create animated')),
)

DISPLAY_CREATIVES_FORMAT_ADBUNDLE_MOBILE_399 = 1
DISPLAY_CREATIVES_FORMAT_BILLBOARD_MEDIUM_RECTANGLE_399 = 2
DISPLAY_CREATIVES_FORMAT_HALFPAGE_399 = 3
DISPLAY_CREATIVES_FORMAT_MEDIUM_RECTANGLE_MOBILE_299 = 4
DISPLAY_CREATIVES_FORMAT_ADBUNDLE_MOBILE_599 = 5
DISPLAY_CREATIVES_FORMAT_BILLBOARD_MEDIUM_RECTANGLE_599 = 6
DISPLAY_CREATIVES_FORMAT_DYNAMIC_SITEBAR = 7
DISPLAY_CREATIVES_FORMAT_HALFPAGE_599 = 8
DISPLAY_CREATIVES_FORMAT_MEDIUM_RECTANGLE_MOBILE_399 = 9
DISPLAY_CREATIVES_FORMAT_CHOICES = Choices(
    (DISPLAY_CREATIVES_FORMAT_ADBUNDLE_MOBILE_399, 'adbundle_mobile_banner_399', _(
        'AdBundle + Mobile Banner (includes the following formats: 160x600, 300x250, 728x90, 320x50) - %(price)d €'
    ) % {'price': 399}),
    (DISPLAY_CREATIVES_FORMAT_BILLBOARD_MEDIUM_RECTANGLE_399, 'billboard_medium_rectangle_399', _(
        'Billboard + Medium Rectangle Presenter (includes the following formats: 800x250, 970x250, 770x250, 300x250)'
        ' - %(price)d €') % {'price': 399}),
    (DISPLAY_CREATIVES_FORMAT_HALFPAGE_399, 'halfpage_ad_399', _(
        'Halfpage Ad (includes the following formats: 300x600, for desktop + mobile) - %(price)d €') % {'price': 399}),
    (DISPLAY_CREATIVES_FORMAT_MEDIUM_RECTANGLE_MOBILE_299, 'medium_rectangle_mobile_299', _(
        'Medium Rectangle + Mobile Banner (includes the following formats: 300x250, 320x50) - %(price)d €'
    ) % {'price': 299}),
    (DISPLAY_CREATIVES_FORMAT_ADBUNDLE_MOBILE_599, 'adbundle_mobile_banner_599', _(
        'AdBundle + Mobile Banner (includes the following formats: 160x600, 300x250, 728x90, 320x50) - %(price)d €'
    ) % {'price': 599}),
    (DISPLAY_CREATIVES_FORMAT_BILLBOARD_MEDIUM_RECTANGLE_599, 'billboard_medium_rectangle_599', _(
        'Billboard + Medium Rectangle Presenter (includes the following formats: 800x250, 970x250, 770x250, 300x250)'
        ' - %(price)d €') % {'price': 599}),
    (DISPLAY_CREATIVES_FORMAT_DYNAMIC_SITEBAR, 'dynamic_site_bar_599', _(
        'Dynamic Sitebar + Medium Rectangle Presenter (includes the following formats: 301x601, 300x250) - %(price)d €'
    ) % {'price': 599}),
    (DISPLAY_CREATIVES_FORMAT_HALFPAGE_599, 'halfpage_ad_599', _(
        'Halfpage Ad (includes the following formats: 300x600, for desktop + mobile) - %(price)d €') % {'price': 599}),
    (DISPLAY_CREATIVES_FORMAT_MEDIUM_RECTANGLE_MOBILE_399, 'medium_rectangle_mobile_399', _(
        'Medium Rectangle + Mobile Banner (includes the following formats: 300x250, 320x50) - %(price)d €'
    ) % {'price': 399}),
)

DISPLAY_AGE_14_19 = 1
DISPLAY_AGE_20_29 = 2
DISPLAY_AGE_30_39 = 3
DISPLAY_AGE_40_49 = 4
DISPLAY_AGE_50_59 = 5
DISPLAY_AGE_60_PLUS = 6
DISPLAY_AGE_CHOICES = Choices(
    (DISPLAY_AGE_20_29, '20_29', _('20-29 years')),
    (DISPLAY_AGE_30_39, '30_39', _('30-39 years')),
    (DISPLAY_AGE_14_19, '14_19', _('14-19 years')),
    (DISPLAY_AGE_40_49, '40_49', _('40-49 years')),
    (DISPLAY_AGE_50_59, '50_59', _('50-59 years')),
    (DISPLAY_AGE_60_PLUS, '60_plus', _('60 years or more')),
)

DISPLAY_GENDER_INDIFFERENT = 1
DISPLAY_GENDER_MALE = 2
DISPLAY_GENDER_FEMALE = 3
DISPLAY_GENDER_CHOICES = Choices(
    (DISPLAY_GENDER_INDIFFERENT, 'indifferent', _('Indifferent')),
    (DISPLAY_GENDER_MALE, 'male', _('Male')),
    (DISPLAY_GENDER_FEMALE, 'female', _('Female')),
)

DISPLAY_TARGETING_ART = 1
DISPLAY_TARGETING_RECRUITING = 2
DISPLAY_TARGETING_TRAVEL = 3
DISPLAY_TARGETING_TECH = 4
DISPLAY_TARGETING_DESIGN = 5
DISPLAY_TARGETING_FASHION = 6
DISPLAY_TARGETING_SPORTS = 7
DISPLAY_TARGETING_AUTOMOBILE = 8
DISPLAY_TARGETING_LUXURY = 9
DISPLAY_TARGETING_CHOICES = Choices(
    (DISPLAY_TARGETING_ART, 'art', _('Art / Culture')),
    (DISPLAY_TARGETING_RECRUITING, 'recruiting', _('Job / Recruiting')),
    (DISPLAY_TARGETING_TRAVEL, 'travel', _('Travel')),
    (DISPLAY_TARGETING_TECH, 'tech', _('Tech')),
    (DISPLAY_TARGETING_DESIGN, 'design', _('Design')),
    (DISPLAY_TARGETING_FASHION, 'fashion', _('Fashion')),
    (DISPLAY_TARGETING_SPORTS, 'sports', _('Sports')),
    (DISPLAY_TARGETING_AUTOMOBILE, 'automobile', _('Automobile')),
    (DISPLAY_TARGETING_LUXURY, 'luxury', _('Luxury')),
)

DISPLAY_CHANNEL_ACTIVE_LIVING = 2
DISPLAY_CHANNEL_AUTOMOTIVE = 3
DISPLAY_CHANNEL_DIGITAL_LIFE = 4
DISPLAY_CHANNEL_ECOMMERCE = 5
DISPLAY_CHANNEL_ENTERTAINMENT = 6
DISPLAY_CHANNEL_FAMILY_AND_KIDS = 7
DISPLAY_CHANNEL_HEALTH = 8
DISPLAY_CHANNEL_LIFESTYLE = 9
DISPLAY_CHANNEL_NEWS = 10
DISPLAY_CHANNEL_SPORTS = 11
DISPLAY_CHANNEL_TRAVEL = 12
DISPLAY_CHANNEL_WOMEN = 14
DISPLAY_CHANNEL_CONSTRUCTION_AND_LIVING = 59
DISPLAY_CHANNEL_MEN = 60
DISPLAY_CHANNEL_EAT_AND_DRINK = 62
DISPLAY_CHANNEL_CHOICES = Choices(
    (DISPLAY_CHANNEL_ACTIVE_LIVING, 'active_living', _('Active Living')),
    (DISPLAY_CHANNEL_AUTOMOTIVE, 'automotive', _('Automotive')),
    (DISPLAY_CHANNEL_DIGITAL_LIFE, 'digital_life', _('Digital Life')),
    (DISPLAY_CHANNEL_ECOMMERCE, 'ecommerce', _('eCommerce')),
    (DISPLAY_CHANNEL_ENTERTAINMENT, 'entertainment', _('Entertainment')),
    (DISPLAY_CHANNEL_FAMILY_AND_KIDS, 'family_and_kids', _('Family & Kids')),
    (DISPLAY_CHANNEL_HEALTH, 'health', _('Health')),
    (DISPLAY_CHANNEL_LIFESTYLE, 'lifestyle', _('Lifestyle')),
    (DISPLAY_CHANNEL_NEWS, 'news', _('News')),
    (DISPLAY_CHANNEL_SPORTS, 'sports', _('Sports')),
    (DISPLAY_CHANNEL_TRAVEL, 'travel', _('Travel')),
    (DISPLAY_CHANNEL_WOMEN, 'women', _('Women')),
    (DISPLAY_CHANNEL_CONSTRUCTION_AND_LIVING, 'construction_and_living', _('Construction & Living')),
    (DISPLAY_CHANNEL_MEN, 'men', _('Men')),
    (DISPLAY_CHANNEL_EAT_AND_DRINK, 'eat_and_drink', _('Eating & Drinking')),
)

INAPP_AUDIENCE_GEBRAUCHTWAGEN_INTERESSENTEN = 1
INAPP_AUDIENCE_B2B_AUTOMOTIVE = 2
INAPP_AUDIENCE_AUTOBESITZER = 3
INAPP_AUDIENCE_SERIENJUNKIES = 4
INAPP_AUDIENCE_HEAVY_STREAMER = 5
INAPP_AUDIENCE_MOVIE_LOVER = 6
INAPP_AUDIENCE_ENTERTAINMENT_LOVER = 7
INAPP_AUDIENCE_CASUAL_GAMER = 8
INAPP_AUDIENCE_ECOMMERCE_SHOPPER = 9
INAPP_AUDIENCE_SMART_SHOPPER_SPARFUCHS_ANGEBOT = 10
INAPP_AUDIENCE_STYLISH_MEN = 11
INAPP_AUDIENCE_HIGH_END_FASHIONISTA = 12
INAPP_AUDIENCE_LOW_BUDGET_FASHIONISTAS = 13
INAPP_AUDIENCE_MOBELFREAKS = 14
INAPP_AUDIENCE_DIY = 15
INAPP_AUDIENCE_AZUBIS_AKTUELLE_AZUBIS = 16
INAPP_AUDIENCE_STUDENTEN_UND_ABSOLVENTEN = 17
INAPP_AUDIENCE_FRAUEN_MIT_KINDERWUNSCH = 18
INAPP_AUDIENCE_KRANKE_MENSCHEN_SCHNIEFNASEN = 19
INAPP_AUDIENCE_GESUNDHEITSINTERESSIERTE = 20
INAPP_AUDIENCE_SCHONHEITS_OP_INTERESSIERTE = 21
INAPP_AUDIENCE_FOTOKUNSTLER = 22
INAPP_AUDIENCE_REISENDE_REISEAFFINE = 23
INAPP_AUDIENCE_FREQUENT_FLYER = 24
INAPP_AUDIENCE_SPORTSKANONEN = 25
INAPP_AUDIENCE_OUTDOOR_LIEBHABER = 26
INAPP_AUDIENCE_MOTORSPORT_FANS = 27
INAPP_AUDIENCE_SMARTHOME = 28
INAPP_AUDIENCE_HAUSBESITZER_VLL_ANGEHENDE_HB = 29
INAPP_AUDIENCE_JOBSUCHENDE = 30
INAPP_AUDIENCE_YOUNG_PROFESSIONALS = 31
INAPP_AUDIENCE_KULTURINTERESSIERTE = 32
INAPP_AUDIENCE_TECHNIKSOFTWARE_INTERESSIERTE = 33
INAPP_AUDIENCE_TECHNIK_LOVER = 34
INAPP_AUDIENCE_HIGH_INCOME_RICH_PEOPLE = 35
INAPP_AUDIENCE_MILLENIALS = 36
INAPP_AUDIENCE_MOMS_KIDS = 37
INAPP_AUDIENCE_FAMILIENVATER = 38
INAPP_AUDIENCE_BEST_AGER = 39
INAPP_AUDIENCE_BOSSHOME = 40
INAPP_AUDIENCE_HOBBYKOCHE = 41
INAPP_AUDIENCE_CHOICES = Choices(
    (INAPP_AUDIENCE_GEBRAUCHTWAGEN_INTERESSENTEN, 'gebrauchtwagen_interessenten', _('Interested in used cars')),
    (INAPP_AUDIENCE_B2B_AUTOMOTIVE, 'b2b_automotive', _('B2B Automotive')),
    (INAPP_AUDIENCE_AUTOBESITZER, 'autobesitzer', _('Car owners')),
    (INAPP_AUDIENCE_SERIENJUNKIES, 'serienjunkies', _('Series junkies')),
    (INAPP_AUDIENCE_HEAVY_STREAMER, 'heavy_streamer', _('Heavy streamers')),
    (INAPP_AUDIENCE_MOVIE_LOVER, 'movie_lover', _('Movie lovers')),
    (INAPP_AUDIENCE_ENTERTAINMENT_LOVER, 'entertainment_lover', _('Entertainment lovers')),
    (INAPP_AUDIENCE_CASUAL_GAMER, 'casual_gamer', _('Casual gamer')),
    (INAPP_AUDIENCE_ECOMMERCE_SHOPPER, 'ecommerce_shopper', _('ecommerce shoppers')),
    (INAPP_AUDIENCE_SMART_SHOPPER_SPARFUCHS_ANGEBOT, 'smart_shopper_sparfuchs_angebot',
     _('Smart shoppers / scrimpers')),
    (INAPP_AUDIENCE_STYLISH_MEN, 'stylish_men', _('Stylish men')),
    (INAPP_AUDIENCE_HIGH_END_FASHIONISTA, 'high_end_fashionista', _('High end fashionista')),
    (INAPP_AUDIENCE_LOW_BUDGET_FASHIONISTAS, 'low_budget_fashionistas', _('Low budget fashionista')),
    (INAPP_AUDIENCE_MOBELFREAKS, 'mobelfreaks', _('Furniture freaks')),
    (INAPP_AUDIENCE_DIY, 'diy', _('DIY')),
    (INAPP_AUDIENCE_AZUBIS_AKTUELLE_AZUBIS, 'azubis_aktuelle_azubis', _('Apprentices')),
    (INAPP_AUDIENCE_STUDENTEN_UND_ABSOLVENTEN, 'studenten_und_absolventen', _('Students and alumni')),
    (INAPP_AUDIENCE_FRAUEN_MIT_KINDERWUNSCH, 'frauen_mit_kinderwunsch', _('Women whishing for children')),
    (INAPP_AUDIENCE_KRANKE_MENSCHEN_SCHNIEFNASEN, 'kranke_menschen_schniefnasen', _('Sick people / runny noses')),
    (INAPP_AUDIENCE_GESUNDHEITSINTERESSIERTE, 'gesundheitsinteressierte', _('Interested in health')),
    (INAPP_AUDIENCE_SCHONHEITS_OP_INTERESSIERTE, 'schonheits_op_interessierte', _('Interested in cosmetic surgery')),
    (INAPP_AUDIENCE_FOTOKUNSTLER, 'fotokunstler', _('Photo artists')),
    (INAPP_AUDIENCE_REISENDE_REISEAFFINE, 'reisende_reiseaffine', _('Travelers / Travel afficionados')),
    (INAPP_AUDIENCE_FREQUENT_FLYER, 'frequent_flyer', _('Frequent flyer')),
    (INAPP_AUDIENCE_SPORTSKANONEN, 'sportskanonen', _('Sporting aces')),
    (INAPP_AUDIENCE_OUTDOOR_LIEBHABER, 'outdoor_liebhaber', _('Outdoor enthusiasts')),
    (INAPP_AUDIENCE_MOTORSPORT_FANS, 'motorsport_fans', _('Motorsport fans')),
    (INAPP_AUDIENCE_SMARTHOME, 'smarthome', _('Smart home')),
    (INAPP_AUDIENCE_HAUSBESITZER_VLL_ANGEHENDE_HB, 'hausbesitzer_vll_angehende_hb',
     _('House owners (or future ones)')),
    (INAPP_AUDIENCE_JOBSUCHENDE, 'jobsuchende', _('Job seakers')),
    (INAPP_AUDIENCE_YOUNG_PROFESSIONALS, 'young_professionals', _('Young professionals')),
    (INAPP_AUDIENCE_KULTURINTERESSIERTE, 'kulturinteressierte', _('Cultural interested')),
    (INAPP_AUDIENCE_TECHNIKSOFTWARE_INTERESSIERTE, 'techniksoftware_interessierte',
     _('Technology/software interested')),
    (INAPP_AUDIENCE_TECHNIK_LOVER, 'technik_lover', _('Tech lovers')),
    (INAPP_AUDIENCE_HIGH_INCOME_RICH_PEOPLE, 'high_income_rich_people', _('High income / rich people')),
    (INAPP_AUDIENCE_MILLENIALS, 'millenials', _('Millenials')),
    (INAPP_AUDIENCE_MOMS_KIDS, 'moms_kids', _('Moms & kids')),
    (INAPP_AUDIENCE_FAMILIENVATER, 'familienvater', _('Dads')),
    (INAPP_AUDIENCE_BEST_AGER, 'best_ager', _('Best ager')),
    (INAPP_AUDIENCE_BOSSHOME, 'bosshome', _('Boss@Home')),
    (INAPP_AUDIENCE_HOBBYKOCHE, 'hobbykoche', _('Amateur chefs')),
)


class AccountSerializer(serializers.Serializer):
    """
    represents a customer
    """

    """
    easys system id of the contact

    """
    easys_id = serializers.IntegerField(required=True)

    """
    salesforce account id of the location

    """
    salesforce_id = serializers.CharField(min_length=15, max_length=18, required=True)

    """
    list of industry topic codes, e.g.
    "011100_3" for "Dienstleistung / Handwerk / Baugewerbe / Ladenbau / Maßmöbel"

    """
    branch_codes = serializers.ListField(
        child=serializers.CharField(max_length=16, required=True), required=True, allow_empty=False)

    """
    generic comment on the customer

    """
    comment = serializers.CharField(max_length=200, allow_blank=True, required=False)

    """
    customer name, this should usually be the full legal name of the customers company

    """
    name = serializers.CharField(max_length=250, required=True)

    """
    company description

    """
    description = serializers.CharField(max_length=200, allow_blank=True, required=False)

    """
    usp describing the customers competitive advantage

    """
    usp = serializers.CharField(max_length=200, allow_blank=True, required=False)

    """
    comprehensive goal of the whole advertisement campaign of the customer

    """
    campaign_goal = serializers.CharField(max_length=200, allow_blank=True, required=False)


class ContactSerializer(serializers.Serializer):
    """
    represents a contact of the customer

        orders.contact_id (contract contact) AND orders.online_deviating_contact_id (additional contact for
        online products)
    """

    """
    easys system id of the contact

    """
    easys_id = serializers.IntegerField(required=True)

    """
    easys system id of the account the contact is related to

    """
    easys_account_id = serializers.IntegerField(required=True)

    """
    salesforce user id of the contact

    """
    salesforce_id = serializers.CharField(min_length=15, max_length=18, allow_blank=True, required=False)

    """
    """
    phone = PhoneNumberField(allow_null=True, required=False)

    """
    """
    email = serializers.EmailField(required=True)

    """
    """
    title = serializers.ChoiceField(choices=TITLE_CHOICES, allow_blank=True, required=False)

    """
    """
    first_name = serializers.CharField(max_length=255, allow_blank=True, required=False)

    """
    """
    last_name = serializers.CharField(max_length=255, allow_blank=True, required=False)

    """
    when is the contact best available
    e.g. craftsmen aren't easy to reach while they're out of office at the customers place doing their job

    """
    opportune_contact_moment = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    is the contact authorized to sign contract on behalf of the company?

    """
    is_authorized_to_sign = serializers.BooleanField(default=False)

    """
    is this the primary contact for the customer?

    """
    is_primary_contact = serializers.BooleanField(default=False)

    """
    will this contact receive reports?

    """
    opt_in_product_reports = serializers.BooleanField(required=True)

    """
    will this contact receive call notifications?

    """
    opt_in_calls = serializers.BooleanField(required=True)

    """
    will this contact receive webform contact notifications?

    """
    opt_in_contact_form = serializers.BooleanField(required=True)

    """
    will this contact receive contract related notifications?

    """
    opt_in_info = serializers.BooleanField(required=True)

    """
    will this contact receive surveys?

    """
    opt_in_evaluations = serializers.BooleanField(required=True)

    """
    is this contact allowed to access the customer area and product statistics?

    """
    is_allowed_statistics = serializers.BooleanField(required=True)


class AccountLocationSerializer(serializers.Serializer):
    """
    represents a physical location or field of activity of the customer

    locations should be used to cluster customers by physical locations (e.g. the berlin or cologne office) or
    by fields of activity (e.g. if a customer has a law consulting business and an import/export business that he both
    wants to advertise for)

    """

    """
    easys system id of the account location

    """
    easys_id = serializers.IntegerField(required=True)

    """
    easys system id of the account that the location is subordinated to

    """
    easys_account_id = serializers.IntegerField(required=True)

    """
    location name
    this is usually the city of the location or the field of activity, see class description
    this location name will also be printed on invoices and be shown in the customer area

    """
    name = serializers.CharField(max_length=255, required=True)

    """
    account owner of the legal entity that is represented by this location

    """
    owner = serializers.CharField(max_length=50, allow_blank=True, required=False)

    """
    plain street name part of address

    """
    street = serializers.CharField(max_length=100, required=True)

    """
    pure house number (integer) part of address

    """
    house_number = serializers.CharField(max_length=10, allow_blank=True, required=False)

    """
    house number addition part of address, e.g. "/1", "a", "Apartment 23"

    """
    house_number_addition = serializers.CharField(max_length=100, allow_blank=True, required=False)

    """
    zip code

    """
    zip_code = serializers.CharField(max_length=10, required=True)

    """
    city name without district

    """
    city = serializers.CharField(max_length=100, required=True)
    """
    country as ISO 3166-1 alpha-2 code
    e.g. DE, ES, AT, CH

    """
    country = CountryField(required=True)

    """
    latitude of location

    """
    geo_latitude = serializers.FloatField(allow_null=True, required=False)

    """
    longitude of location

    """
    geo_longitude = serializers.FloatField(allow_null=True, required=False)

    """
    id of the google places dataset of that location

    """
    google_places_id = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    is this the primary location of the customer?

    """
    is_primary_location = serializers.BooleanField(required=False)

    """
    plain street name part of billing address

    billing address information must always be provided even if it just duplicates the location address

    """
    billing_street = serializers.CharField(max_length=100, allow_blank=True, required=True)

    """
    pure house number (integer) part of billing address

    billing address information must always be provided even if it just duplicates the location address

    """
    billing_house_number = serializers.CharField(max_length=10, allow_blank=True, required=False)

    """
    house number addition part of billing address, e.g. "/1", "a", "Apartment 23"

    billing address information must always be provided even if it just duplicates the location address

    """
    billing_house_number_addition = serializers.CharField(max_length=100, allow_blank=True, required=False)

    """
    billing zip code

    billing address information must always be provided even if it just duplicates the location address

    """
    billing_zip_code = serializers.CharField(max_length=10, required=True)

    """
    billing city name without district

    billing address information must always be provided even if it just duplicates the location address

    """
    billing_city = serializers.CharField(max_length=100, required=True)

    """
    billing country as ISO 3166-1 alpha-2 code

    billing address information must always be provided even if it just duplicates the location address

    """
    billing_country = CountryField(required=True)

    """
    title of billing contact

    """
    billing_title = serializers.ChoiceField(choices=TITLE_CHOICES, required=True, allow_null=True)

    """
    first name of billing contact

    """
    billing_first_name = serializers.CharField(max_length=255, required=True)

    """
    last name of billing contact

    """
    billing_last_name = serializers.CharField(max_length=255, required=True)

    """
    phone number of billing contact

    """
    billing_phone = PhoneNumberField(allow_null=True, required=False)

    """
    email address to sent invoices and other billing documents to
    let blank if billing documents should be sent by classic mail

    """
    billing_email = serializers.EmailField(allow_blank=True, required=False)

    """
    is the customer freed from paying tax?

    """
    billing_no_tax = serializers.BooleanField(required=True)

    """
    customer vat number to be added to the invoice for input tax deduction

    """
    billing_vat_number = serializers.CharField(
        max_length=16, allow_blank=True, required=False, validators=[VATNumberValidator()])

    """
    payment method of the customer, currently charge and transfer are supported

    """
    payment_type = serializers.ChoiceField(choices=PAYMENT_METHOD_CHOICES, required=True)

    """
    iban of the customers bank account that will be charged

    data must be provided if payment_type == PAYMENT_METHOD_CHARGE
    let blank for all other payment methods

        orders.billing_contact_id)
    """
    payment_debit_account_iban = serializers.CharField(
        max_length=34, allow_blank=True, required=False, validators=[IBANValidator()])

    """
    owner of the customers bank account that will be charged

    data must be provided if payment_type == PAYMENT_METHOD_CHARGE
    let blank for all other payment methods

        else relate to orders.billing_company_id)
    """
    payment_debit_account_owner = serializers.CharField(max_length=70, allow_blank=True, required=False)

    """
    true if customer agree in being used as a reference customer
    """
    reference_customer = serializers.BooleanField(default=False)

    def validate(self, data):
        if data.get('payment_type') == PAYMENT_METHOD_CHARGE and not data.get('payment_debit_account_iban'):
            raise serializers.ValidationError('payment_type Charge requires payment_debit_account_iban')
        return data


class OrderLineGoogleAdsBasicSerializer(serializers.Serializer):
    """
    detailed specifications and briefing information for a google ads basic product - "google_basic" product subtype
    """

    """
    what goals should be reached with the advertisement campaign?
    e.g. get new customers, spread word about a product, etc.
    """
    campaign_goal = serializers.CharField(max_length=200, allow_blank=True, required=False)

    """
    the expected impression share when the campaign budget is initially calculated
    """
    expected_impression_share = serializers.DecimalField(
        decimal_places=2, max_digits=5, allow_null=True, required=False)

    """
    the expected impressions when the campaign budget is initially calculated
    """
    expected_impressions = serializers.CharField(max_length=50, allow_blank=True, required=False)

    """
    which cities/regions should the ad be targeted on?
    """
    regions = serializers.ListField(
        child=serializers.CharField(max_length=100, required=True), required=True, allow_empty=False)

    """
    customer preferred keywords to be found on with his campaign
    """
    keywords = serializers.ListField(child=serializers.CharField(max_length=100, required=True), required=True)

    """
    list of keywords that resulted in zero search volume on campaign calculation
    these keywords will not be guaranteed to be included in the campaign
    """
    keywords_with_zero_search_volume = serializers.ListField(child=serializers.CharField(max_length=100, required=True),
                                                             required=True)

    """
    definition of the target group this google ads campaign should be focused on
    """
    target_audience = serializers.CharField(max_length=1000, required=True)

    """
    chose which type of target page should be used in the ad? new or existing website
    """
    target_page_type = serializers.ChoiceField(choices=GOOGLE_ADS_LANDING_PAGE_CHOICES, required=False)

    """
    url of the ads target website if CUSTOMER_WEBSITE is chosen in target_page_type
    """
    target_url = serializers.URLField(allow_blank=True, required=False)


class OrderLineGoogleAdsPremiumSerializer(serializers.Serializer):
    """
    detailed specifications and briefing information for a google ads premium product - "adwords" product subtype
    """

    """
    call to action text, e.g. "Need help? Call us now"
    """
    call_to_action = serializers.CharField(max_length=200, allow_blank=True, required=False)

    """
    what goals should be reached with the advertisement campaign?
    e.g. get new customers, spread word about a product, etc.
    """
    campaign_goal = serializers.CharField(max_length=200, allow_blank=True, required=False)

    """
    the expected clicks when the campaign budget is initially calculated
    """
    expected_clicks = serializers.IntegerField(required=True)

    """
    the expected conversions when the campaign budget is initially calculated
    """
    expected_conversions = serializers.IntegerField(required=True)

    """
    which cities/regions should the ad be targeted on?
    """
    regions = serializers.ListField(child=serializers.CharField(max_length=100, required=True), required=True)

    """
    customer preferred keywords to be found on with his campaign
    """
    keywords = serializers.ListField(child=serializers.CharField(max_length=100, required=True), required=True)

    """
    customer preferred topics (branch_codes) from which the keywords will be used to build his campaigns
    """
    branch_codes = serializers.ListField(child=serializers.CharField(max_length=100, required=True), required=False)

    """
    list of keywords that resulted in zero search volume on campaign calculation
    these keywords will not be guaranteed to be included in the campaign
    """
    keywords_with_zero_search_volume = serializers.ListField(child=serializers.CharField(max_length=100, required=True),
                                                             required=True)

    """
    definition of the target group this google ads campaign should be focused on
    """
    target_audience = serializers.CharField(max_length=1000, required=True)

    """
    usp describing the customers competitive advantage that should get a focus in the campaign texts
    """
    usp = serializers.CharField(max_length=1000, required=True)

    """
    chose which type of target page should be used in the ad? new or existing website
    """
    target_page_type = serializers.ChoiceField(choices=GOOGLE_ADS_LANDING_PAGE_CHOICES, required=False)

    """
    url of the ads target website if CUSTOMER_WEBSITE is chosen in target_page_type
    """
    target_url = serializers.URLField(allow_blank=True, required=False)

    """
    specifies if campaign will be tracked or not.
    This is true in case if customer has campaign tracking booked for Stroer Website.
    If campaign tracking for customer Website than field is false and new detail_customer_website order has to be added.
    RH: must book an additional call tracking number
    """
    call_tracking = serializers.BooleanField(required=True)

    """
    does the customer already have a google ads account that we should take over and optimize, provide the account id
    """
    existing_account_id = serializers.CharField(max_length=10, allow_blank=True, required=False)

    """
    does the customer want to have a remarketing campaign included?
    """
    include_remarketing = serializers.BooleanField(required=False)

    """
    if remarketing campaign is booked (include_remarketing=True) this id its own separate setup fee
    """
    remarketing_setup_fee = serializers.DecimalField(decimal_places=2, max_digits=10, allow_null=True, required=False)

    """
    if remarketing campaign is booked (include_remarketing=True) this id its own separate budget
    """
    remarketing_budget = serializers.DecimalField(decimal_places=2, max_digits=10, allow_null=True, required=False)

    """
    the expected impression share when the campaign budget is initially calculated
    """
    expected_impression_share = serializers.DecimalField(
        decimal_places=2, max_digits=5, allow_null=True, required=False)

    """
    the expected impressions when the campaign budget is initially calculated
    """
    expected_impressions = serializers.CharField(max_length=50, allow_blank=True, required=False)

    def validate(self, data):
        if data.get('include_remarketing') and data.get('remarketing_setup_fee') is None:
            raise serializers.ValidationError(
                {'remarketing_setup_fee': 'value >= 0 must be provided when include_remarketing is true'}
            )
        if data.get('include_remarketing') and not data.get('remarketing_budget'):
            raise serializers.ValidationError(
                {'remarketing_budget': 'value > 0 must be provided when include_remarketing is true'}
            )
        return data


class OrderLineDisplayBasicSerializer(serializers.Serializer):
    """
    detailed specifications and briefing information for a display basic product - "display_web_continuous_rif" subtype
    """

    """
    impressions per month, used by basic (20000/40000/80000/etc impressions) or continuous premium product

        Please also provide field values for
        products.product_type
        order_line_online_details.banner_booking_type
    """
    impressions_per_month = serializers.ChoiceField(choices=DISPLAY_IMPRESSIONS_PER_MONTH_CHOICES,
                                                    required=False, allow_null=True)

    """
    german zip codes used for geographical targeting
    RH: must be converted to our geo targeting format

    HC: the zip code together with geo_targeting_radius must be converted to our targeting json format
    """
    geo_targeting_zip = serializers.CharField(max_length=5, required=False, allow_blank=True)

    """
    what radius (km) around the geographical focus are described in geo_targeting should be targeted?
    """
    geo_targeting_radius = serializers.IntegerField(min_value=1, max_value=80, required=False)

    """
    what goals should be reached with the advertisement campaign?
    e.g. get new customers, spread word about a product, etc.
    """
    campaign_goal = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    headline text that will be shown on the creative
    """
    headline = serializers.CharField(max_length=40, required=True)

    """
    sub-headline text that will be shown on the creative
    """
    sub_headline = serializers.CharField(max_length=40, required=True)

    """
    list of bullet point texts that will be shown on the creative
    """
    bullet_points = serializers.ListField(child=serializers.CharField(max_length=100), required=True)

    """
    call to action text that will be shown on the creative
    """
    call_to_action = serializers.CharField(max_length=18, required=True)

    """
    choice for the type of banner color selection: from website or color picker for e.g. color_code_1
    """
    banner_color_selection = serializers.ChoiceField(choices=DISPLAY_BANNER_COLOR_SELECTION_CHOICES,
                                                     required=False, allow_blank=True)

    """
    color code to be used when designing the creative (priority 1)
    """
    color_code_1 = serializers.CharField(max_length=7, allow_blank=True, required=False)

    """
    color code to be used when designing the creative (priority 2)
    """
    color_code_2 = serializers.CharField(max_length=7, allow_blank=True, required=False)

    """
    color code to be used when designing the creative (priority 3)

    """
    color_code_3 = serializers.CharField(max_length=7, allow_blank=True, required=False)

    """
    choice for the source where the banner images should be used from: customer, website, rehiohelden
    """
    banner_image_selection = serializers.ChoiceField(choices=DISPLAY_BANNER_IMAGE_SOURCE_CHOICES, required=True)

    """
    chose which type of target page should be used in the ad? new or existing website
    """
    target_page_type = serializers.ChoiceField(choices=LANDING_PAGE_CHOICES, required=False)

    """
    url of the ads target website if CUSTOMER_WEBSITE is chosen in target_page_type
    """
    target_url = serializers.URLField(allow_blank=True, required=False)

    """
    creative template selected for basic product variant, will be ignored in premium and professional types
    EASYS: order_line_online_details.banner_layout
    """
    package_template = serializers.IntegerField(allow_null=True, required=False)

    """
    what location should be added to the location framing of the creative?
    only used in basic product variant

    EASYS: order_line_online_details.banner_location_frame
    """
    location_frame_text = serializers.CharField(max_length=50, allow_blank=True, required=False)

    """
    will the customer provide creatives or do we have to create new ones?
    if new ones must be created, chose which type

    EASYS: order_line_online_details.banner_option
    HC: ProductDisplay.premium_for_html5 (true if CREATIVE_OPTION_CREATE_ANIMATED, false otherwise)
    """
    creative_options = serializers.ChoiceField(choices=DISPLAY_BASIC_CREATIVE_OPTION_CHOICES, required=True)

    def validate(self, data):
        if data.get('geo_targeting') and not data.get('geo_targeting_radius'):
            raise serializers.ValidationError('Geo targeting radius is mandatory')
        return data


class OrderLineDisplayPremiumSerializer(serializers.Serializer):
    """
    detailed specifications and briefing information for a display premium product
    - any of the display web/mobile fix/continuous subtypes
    """

    """
    campaign type, fixed runtime or continuous advertisement
    """
    booking_type = serializers.ChoiceField(choices=BOOKING_TYPE_CHOICES, required=True)

    """
    which devices should this campaign be run on, web+mobile or mobile only?
    """
    target_devices = serializers.ChoiceField(choices=DISPLAY_TYPE_CHOICES, required=True)

    """
    expected formats of the creative used in the campaign, some formats will incur an additional fee
    """
    creatives_format = serializers.ChoiceField(choices=DISPLAY_CREATIVES_FORMAT_CHOICES, required=True)

    """
    impressions per day, used for fixed runtime premium product
    """
    impressions_per_day = serializers.IntegerField(allow_null=True, required=False)

    """
    impressions per month, used by basic (20000/40000/80000/etc impressions) or continuous premium product

        Please also provide field values for
        products.product_type
        order_line_online_details.banner_booking_type
    """
    impressions_per_month = serializers.IntegerField(allow_null=True, required=False)

    """
    age range selection the ad should be targeted on
    """
    age_targeting = serializers.MultipleChoiceField(choices=DISPLAY_AGE_CHOICES, allow_empty=True, required=True)

    """
    gender selection the ad should be targeted on
    """
    gender_targeting = serializers.ChoiceField(choices=DISPLAY_GENDER_CHOICES, allow_blank=True, required=False)

    """
    list of german zip codes used for geographical targeting
    RH: must be converted to our geo targeting format

    HC: the zip code list must be converted to our targeting json format
    """
    geo_targeting = serializers.ListField(child=serializers.CharField(max_length=10, required=True),
                                          allow_empty=True, required=True)

    """
    list of channel names the ad will be targeted on
    """
    channel_targeting = serializers.MultipleChoiceField(
        choices=DISPLAY_CHANNEL_CHOICES, required=True, allow_empty=True)

    """
    list of interests the ad will be targeted on
    """
    interest_targeting = serializers.MultipleChoiceField(
        choices=DISPLAY_TARGETING_CHOICES, required=False, allow_empty=True)

    """
    what goals should be reached with the advertisement campaign?
    e.g. get new customers, spread word about a product, etc.
    """
    campaign_goal = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    chose which type of target page should be used in the ad? new or existing website
    """
    target_page_type = serializers.ChoiceField(choices=LANDING_PAGE_CHOICES, required=True)

    """
    url of the ads target website if CUSTOMER_WEBSITE is chosen in target_page_type
    """
    target_url = serializers.URLField(allow_blank=True, required=False)

    """
    will the customer provide creatives or do we have to create new ones?
    if new ones must be created, chose which type

    EASYS: order_line_online_details.banner_option
    HC: ProductDisplay.premium_for_html5 (true if CREATIVE_OPTION_CREATE_ANIMATED, false otherwise)
    """
    creative_options = serializers.ChoiceField(choices=CREATIVE_OPTION_CHOICES, required=True)


class OrderLineFacebookDetailedTargetingSerializer(serializers.Serializer):
    """
    definition of a facebook ad detail targeting

    HC: detailed targeting will be merged in a single json structure
    """

    """
    targeting category type
    """
    category = serializers.ChoiceField(choices=FACEBOOK_DETAILED_TARGETS_CATEGORY_CHOICES, required=True)

    """
    description of the targeting criteria
    """
    content = serializers.CharField(max_length=250, required=True)


class OrderLineFacebookSerializer(serializers.Serializer):
    """
    detailed specifications and briefing information for a facebook product
    """

    """
    campaign type, fixed runtime or continuous advertisement

    """
    booking_type = serializers.ChoiceField(choices=BOOKING_TYPE_CHOICES, required=True)

    """
    what goals should be reached with the advertisement campaign?
    e.g. get new customers, spread word about a product, etc.

    """
    campaign_goal = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    does the customer allow usage of stock images?

    EASYS: order_line_online_details.facebook_image_stock
    """
    stock_images_allowed = serializers.BooleanField(required=True)

    """
    do we have to create a new facebook page or can we use an existing easys?

    """
    create_page = serializers.BooleanField(required=True)

    """
    link to existing facebook page, only if create_page is false

    """
    page_url = serializers.URLField(allow_blank=True, required=False)

    """
    login email to existing facebook page account, only if create_page is false

    """
    page_login_email = serializers.EmailField(allow_blank=True, required=False)

    """
    chose which type of target page should be used in the ad? new or existing website

    """
    target_page_type = serializers.ChoiceField(choices=LANDING_PAGE_CHOICES, required=True)

    """
    url of the ads target website if CUSTOMER_WEBSITE is chosen in target_page_type

    """
    target_url = serializers.URLField(allow_blank=True, required=False)

    """
    shall the ad also be shown on instagram or only on facebook?

    """
    include_instagram = serializers.BooleanField(required=True)

    """
    the potential reach when the campaign budget is initially calculated

    """
    potential_reach = serializers.IntegerField(min_value=1, required=True)

    """
    define who's creating texts for the facebook page

    """
    text_source = serializers.ChoiceField(choices=FACEBOOK_TEXT_SOURCE_CHOICES, required=True)

    """
    define who's creating texts for the facebook page

    """
    image_source = serializers.ChoiceField(choices=FACEBOOK_IMAGE_SOURCE_CHOICES, required=True)

    """
    list of marketing target the customer wants to achieve with this campaign

    """
    marketing_targets = serializers.MultipleChoiceField(choices=FACEBOOK_MARKETING_TARGET_CHOICES, required=True)

    """
    age range selection the ad should be targeted on

    """
    age_targeting = serializers.MultipleChoiceField(choices=FACEBOOK_AGE_CHOICES, required=True)

    """
    description of the geographical focus area the ad should be targeted on

    """
    geo_targeting = serializers.CharField(max_length=250, allow_blank=True, required=False)

    """
    what radius (km) around the geographical focus are described in geo_targeting should be targeted?

    """
    geo_targeting_radius = serializers.IntegerField(min_value=1, max_value=80, required=True)

    """
    gender selection the ad should be targeted on

    """
    gender_targeting = serializers.ChoiceField(choices=FACEBOOK_GENDER_CHOICES, required=True)

    """
    list of detailed targeting criterea

    """
    detailed_targeting = OrderLineFacebookDetailedTargetingSerializer(many=True, allow_null=True, required=False)

    """
    is this campaign meant for a special event? add some description to help the ad team find the
    right wording and targeting

    """
    special_events_campaign = serializers.CharField(max_length=250, allow_blank=True, required=False)

    """
    redmine ticket id of the original facebook offer inquiry

    """
    ticket_id = serializers.CharField(max_length=20, required=True)


class OrderLineInAppSerializer(serializers.Serializer):
    """
    detailed specifications and briefing information for an in app product
    """

    """
    detailed briefing information

    """
    briefing = serializers.CharField(max_length=200, allow_blank=True, required=False)

    """
    what goals should be reached with the advertisement campaign?
    e.g. get new customers, spread word about a product, etc.

    """
    campaign_goal = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    impressions to be delivered during the whole campaign runtime

    """
    impressions = serializers.IntegerField(required=True)

    """
    description of the geographical focus area the ad should be targeted on

    """
    geo_targeting = serializers.CharField(max_length=10000, allow_blank=True, required=False)

    """
    description of the audience the ad should be targeted on

    """
    target_audiences = serializers.MultipleChoiceField(choices=INAPP_AUDIENCE_CHOICES, required=False, allow_blank=True)

    """
    textual representation of target audience requirements that are not represented by
    the structured data in target_audiences

    """
    other_target_audiences = serializers.CharField(max_length=10000, required=False, allow_blank=True)

    """
    chose which type of target page should be used in the ad? new or existing website

    """
    target_page_type = serializers.ChoiceField(choices=LANDING_PAGE_CHOICES, required=True)

    """
    url of the ads target website if CUSTOMER_WEBSITE is chosen in target_page_type

    """
    target_url = serializers.URLField(allow_blank=True, required=False)

    """
    selection on who will be providing the creatives

    """
    creatives_creator = serializers.ChoiceField(choices=INAPP_BANNERS_CREATOR_CHOICES, required=True)

    """
    what type of creatives shall be created if new ones are chosen in media_creator?
    true for html5, false for usual image creatives

    """
    creatives_html5 = serializers.BooleanField(required=True)

    """
    what type of creative must be created/provided?

    """
    creatives_template = serializers.ChoiceField(choices=INAPP_BANNER_TEMPLATE_CHOICES, required=True)

    """
    redmine ticket id of the original in app offer inquiry

    """
    ticket_id = serializers.CharField(max_length=20, required=True)

    def validate(self, data):
        if not data.get('target_audiences') and not data.get('other_target_audiences'):
            raise serializers.ValidationError('target_audiences or other_target_audiences has to be set')
        return data


class OrderLineListingOpeningHoursSerializer(serializers.Serializer):
    """
    definition of listing open hours for a single day of week

    mode of operation decides what time values are accepted:
    OPENING_HOURS_MODE_OPEN
        one opening slot accepted -> morning_from/morning_to
    OPENING_HOURS_MODE_OPEN_MORNING_AFTERNOON
        two opening slots accepted -> morning_from/morning_to and afternoon_from/afternoon_to
    OPENING_HOURS_MODE_OPEN_24_HOURS
        no opening slots accepted
    OPENING_HOURS_MODE_CLOSED
        no opening slots accepted
    """

    """
    day of week that opening hour definition is meant for

    """
    day_of_week = serializers.ChoiceField(choices=OPENING_HOURS_WEEK_DAY_CHOICES, required=True)

    """
    opening hour definition type

    """
    mode = serializers.ChoiceField(choices=OPENING_HOURS_MODE_CHOICES, required=True)

    """
    first period begin

    """
    morning_from = serializers.TimeField(allow_null=True, required=False)

    """
    first period end

    """
    morning_to = serializers.TimeField(allow_null=True, required=False)

    """
    second period begin

    """
    afternoon_from = serializers.TimeField(allow_null=True, required=False)

    """
    second period end

    """
    afternoon_to = serializers.TimeField(allow_null=True, required=False)


class OrderLineListingSerializer(serializers.Serializer):
    """
    detailed specifications and briefing information for a listing product
    """

    """
    company description

    """
    company_description = serializers.CharField(max_length=255, allow_blank=True, required=False)

    """
    public company email address published in the directories

    """
    email = serializers.EmailField(required=True)

    """
    public company phone number published in the directories

    """
    phone = PhoneNumberField(required=True)

    """
    public company fax number published in the directories

    """
    fax = PhoneNumberField(allow_null=True, required=False)

    """
    company website url published in the directories

    """
    url = serializers.URLField(allow_blank=True, required=False)

    """
    list of opening hour descriptions for a single day of week each
    each day of week must only be included once, missing days of week will be marked as closed

    """
    opening_hours = OrderLineListingOpeningHoursSerializer(many=True, allow_null=True, required=False)

    """
    additional opening hours information that don't match the structured ones
    e.g. open on request, open only during lunar eclipses, etc.

    """
    opening_hours_description = serializers.CharField(max_length=140, allow_blank=True, required=False)

    """
    list of keywords that will be submitted to directories to classify the company

    """
    keywords = serializers.ListField(child=serializers.CharField(max_length=55, required=True), allow_empty=True,
                                     required=True)

    """
    costs for t-online product
    if this number not a 0 than will be created a t-online product on the same location

    """
    tonline_costs = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)

    """
    city name for t-online product

    """
    tonline_city = serializers.CharField(max_length=100, required=False)

    def validate(self, data):
        self.validate_unique_opening_hours(data['opening_hours'])
        return data

    def validate_unique_opening_hours(self, opening_hours):
        opening_hours = opening_hours or []
        checked_days = []
        for day_schedule in opening_hours:
            if day_schedule['day_of_week'] in checked_days:
                raise serializers.ValidationError(
                    'Multiple opening hours found set for day of week {}.'.format(day_schedule['day_of_week'])
                )
            else:
                checked_days.append(day_schedule['day_of_week'])


class OrderLineSeoSerializer(serializers.Serializer):
    """
    detailed specifications and briefing information for a seo product
    """

    """
    which cms is used on the target website?

    """
    cms = serializers.CharField(max_length=50, allow_blank=True, required=False)

    """
    count of physical locations the optimization should be deasys for

    """
    location_count = serializers.IntegerField(required=True)

    """
    chose which type of target page should be used in the ad? new or existing website

    """
    target_page_type = serializers.ChoiceField(choices=LANDING_PAGE_CHOICES, required=True)

    """
    url of the target website if CUSTOMER_WEBSITE is chosen in target_page_type

    """
    target_url = serializers.URLField(allow_blank=True, required=False)

    """
    credentials to access the target page if CUSTOMER_WEBSITE is chosen in target_page_type

    """
    target_page_credentials = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    topics to optimize for

    """
    topics = serializers.ListField(
        child=serializers.CharField(max_length=100, required=True), required=True, allow_empty=False)

    """
    regions to optimize for

    """
    regions = serializers.ListField(
        child=serializers.CharField(max_length=100, required=True), required=True, allow_empty=False)

    """
    main focus of the seo optimization, which of the customers products/services is the most important?

    """
    focus = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    usp describing the customers competitive advantage that should get a focus in the optimization

    """
    usp = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    keywords that the customer prefers to be higher ranked

    """
    keywords = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    wording style to be used on text optimization

    """
    wording_style = serializers.ChoiceField(choices=SEO_TEXT_STYLE_CHOICES, allow_null=True, required=False)

    """
    redmine ticket id of the original seo offer inquiry

    """
    ticket_id = serializers.CharField(max_length=20, required=True)


class OrderLineLandingpageSerializer(serializers.Serializer):
    """
    information for a Landingpage product
    """

    """
    count of additionally booked subpages
    """
    additional_subpages = serializers.IntegerField(required=True, min_value=0)

    """
    should a new logo be created for the customer?
    """
    logo_creation = serializers.ChoiceField(choices=LOGO_CREATION_CHOICES, required=True)


class OrderLineWebsiteSerializer(serializers.Serializer):
    """
    detailed specifications and briefing information for a website product
    """

    """
    count of included subpages

    """
    included_subpages = serializers.IntegerField(required=True)

    """
    count of addtionally booked subpages

    """
    additional_subpages = serializers.IntegerField(required=True, min_value=0, max_value=60)

    """
    customer desired domain name

    """
    desired_domain = serializers.CharField(max_length=100, validators=[DomainNameValidator()], required=True)

    """
    how should the desired_domain be connected to the website product
    this can either be by registering a new domain, transferring and existing one or using an external domain

    HC: DOMAIN_TYPE_TRANSFER -> ProductDomain.domain_transfer true
        ProductDomain.provider to ProductDomain.PROVIDER_CHOICES.external
    """
    domain_type = serializers.ChoiceField(choices=DOMAIN_TYPE_CHOICES, required=True)

    """
    additional info about the domain

    """
    domain_info = serializers.CharField(max_length=100, allow_blank=True, required=False)

    """
    website briefing about subpages and content

    """
    briefing = serializers.CharField(max_length=200, required=True)

    """
    color code to be used when designing the creative (priority 1)

    """
    color_code_1 = serializers.CharField(
        max_length=7, allow_blank=True, required=False, validators=[HexColorValidator()])

    """
    color code to be used when designing the creative (priority 2)

    """
    color_code_2 = serializers.CharField(
        max_length=7, allow_blank=True, required=False, validators=[HexColorValidator()])

    """
    color code to be used when designing the creative (priority 3)

    """
    color_code_3 = serializers.CharField(
        max_length=7, allow_blank=True, required=False, validators=[HexColorValidator()])

    """
    should a new logo be created for the customer?

    """
    logo_creation = serializers.ChoiceField(choices=LOGO_CREATION_CHOICES, required=True)

    """
    what kind of logo should be created if logo_creation is set to LOGO_CREATION_NEW

    """
    logo_type = serializers.ChoiceField(choices=LOGO_TYPE_CHOICES, allow_null=True, required=False)

    """
    textual description of wishes and requirements for the logo

    """
    logo_description = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    website design choice between minimalistic and embellished

    """
    design_preference_minimalistic_embellished = serializers.ChoiceField(
        choices=WEBSITE_DESIGN_PREFERENCE_MINIMALISTIC_EMBELLISHED, allow_null=True, required=False)

    """
    website design choice between modern and classic

    """
    design_preference_modern_classic = serializers.ChoiceField(
        choices=WEBSITE_DESIGN_PREFERENCE_MODERN_CLASSIC, allow_null=True, required=False)

    """
    website design choice between simple and striking

    """
    design_preference_simple_striking = serializers.ChoiceField(
        choices=WEBSITE_DESIGN_PREFERENCE_SIMPLE_STRIKING, allow_null=True, required=False)

    """
    website design choice between text and picture

    """
    design_preference_text_picture = serializers.ChoiceField(
        choices=WEBSITE_DESIGN_PREFERENCE_TEXT_PICTURE, allow_null=True, required=False)

    """
    textual description of wishes and requirements for the website design

    """
    design_preferences = serializers.CharField(max_length=1000, allow_blank=True, required=False)

    """
    what goals should be reached with the new website?
    e.g. get new customers, spread word about a product, etc.

    """
    campaign_goal = serializers.CharField(max_length=1000, allow_blank=True, required=False)


class OrderLineEmailSerializer(serializers.Serializer):
    """
    detailed specifications and briefing information for an email product
    """

    """
    count of included email accounts

    """
    included_accounts = serializers.IntegerField(required=True)

    """
    count of additionally booked email accounts

    """
    additional_accounts = serializers.IntegerField(required=True)

    """
    list of the actual email account names

    """
    addresses = serializers.ListField(child=serializers.EmailField(required=True))


class OrderLineCustomerWebsiteSerializer(serializers.Serializer):
    """
    detailed specifications and briefing information for an external website product

    RH: always book an onsite product in this case
    """

    """
    url of the customer website used as an advertisement target

    """
    url = serializers.URLField(required=True)


class OrderLineSerializer(serializers.Serializer):
    """
    represents an item in the order a.k.a. a product
    """

    """
    easys system id of the order line

    """
    easys_id = serializers.IntegerField(required=True)

    """
    easys system id of the order the order line is subordinated to

    """
    easys_order_id = serializers.IntegerField(required=True)

    """
    easys system id of the location the order line is subordinated to

    """
    easys_account_location_id = serializers.IntegerField(required=True)

    """
    overall rebate percentage contained in the final prices of the orderline

    """
    rebate_percentage = serializers.DecimalField(decimal_places=2, max_digits=10, allow_null=True, required=False)

    """
    setup fee will be invoiced as soon as the service call has been completed with the customer

    EASYS: orderline_online_details.web_site_pricing_logo (50%, rest is start_fee)
    EASYS: orderline_online_details.web_site_pricing_web_sites (50%, rest is start_fee)
    EASYS: orderline_online_details.adwords_pricing_remarketing
    EASYS: facebook setup cost if facebook page is created by provider @dominikus

    """
    setup_fee = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)

    """
    postponed setup fee used for fixed-runtime campaigns that will only be invoiced
    once, three weeks before the product is activated.

    EASYS: InApp banner creation cost
    EASYS: display banner creation cost if booking_type == BOOKING_TYPE.fixed
    """
    # TODO: set required=True when all usages updated
    postponed_setup_fee = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)

    """
    start fee will be invoiced as soon as the product is activated
    e.g. if website setup cost is splitted 50/50 by setup and start fee

    EASYS: orderline_online_details.web_site_pricing_logo (50%, rest is setup_fee)
    EASYS: orderline_online_details.web_site_pricing_web_sites (50%, rest is setup_fee)
    """
    start_fee = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)

    """
    gross advertisement budget will be invoiced on a monthly basis
    the net budget is calculated using the provided commission

    EASYS: orderline_online_details.adwords_budget
    EASYS: orderline_online_details.seo_budget
        (OrderLineFacebookSerializer.booking_type == BOOKING_TYPE_CONTINUOUS)

    """
    budget = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)

    """
    operational costs that will be invoiced on a monthly basis

    EASYS: orderline_online_details.web_site_pricing_email
    EASYS: orderline_online_details.adwords_pricing_call_tracking

    """
    fee = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)

    """
    gross one-off advertisement budget used for fixed runtime campaigns that will only be invoiced once
    the net budget is calculated using the provided commission

    EASYS: orderline_online_details.banner_budget (premium fixed runtime ads)
        (OrderLineFacebookSerializer.booking_type == BOOKING_TYPE_FIXED)

    """
    one_time_budget = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)

    """
    agency commission percentage to calculate net budget from gross budget

    """
    commission = serializers.DecimalField(decimal_places=2, max_digits=5, required=False)

    """
    overall sum of deferred payment that will be sent as one invoice to the customer but can be payed over
    several months, see deferred_payment_months

    """
    deferred_payment_sum = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)

    """
    duration of the deferred payment in months, the monthly costs are calculated as
    deferred_payment_sum / deferred_payment_months

    """
    deferred_payment_months = serializers.IntegerField(min_value=1, required=True, allow_null=True)

    """
    general comment on the order

    """
    comment = serializers.CharField(max_length=300, allow_blank=True, required=False)

    """
    customer preferred product start date or definitive start date for fixed runtime products

    """
    start_date = serializers.DateField(allow_null=True, required=True)

    """
    end date for fixed runtime products

    """
    end_date = serializers.DateField(allow_null=True, required=False)

    """
    product type the orderline is meant for, additional detail information must be provided in
    the appropriate sub-serializer

    HC: combination of product_type and product_level will lead to specific product subtype
    """
    product_type = serializers.ChoiceField(choices=PRODUCT_TYPE_CHOICES, required=True)

    """
    product level that determines functionality and features of a product
    depending on the product level, different information has to be provided in the appropriate sub-serializer

    HC: combination of product_type and product_level will lead to specific product subtype
    """
    product_level = serializers.ChoiceField(choices=PRODUCT_LEVEL_CHOICES, required=True, allow_null=True)

    """
    minimum initial contract duration in months

    """
    initial_term_months = serializers.IntegerField(min_value=1, required=True)

    """
    notice period during the initial contract term as months,days (e.g. 2,14)

    """
    first_cancellation_period = serializers.CharField(max_length=5, validators=[validate_comma_separated_integer_list,
                                                                                comma_separated_period_validatior],
                                                      allow_blank=True,
                                                      required=False)

    """
    notice period during extended contract terms as months,days (e.g. 2,14)

    """
    cancellation_period = serializers.CharField(max_length=5, validators=[validate_comma_separated_integer_list,
                                                                          comma_separated_period_validatior],
                                                allow_blank=True,
                                                required=False)

    """
    contract revocation period after product has been started, only valid for MDS customers as months,days (e.g. 2,14)

    ONE: will not be provided in the beginning and default has to be calculated on HC side
    """
    # this is a special case for mds customers
    early_cancellation_period = serializers.CharField(max_length=5, validators=[validate_comma_separated_integer_list,
                                                                                comma_separated_period_validatior],
                                                      allow_blank=True,
                                                      required=False)

    """
    invoicing period of the product (in months)
    """
    payment_cycle = serializers.ChoiceField(choices=PRODUCT_PAYMENT_CYCLE_CHOICES, required=False)

    """
    sub-serializer for google ads basic specific product data ("google_basic" product subtype)
    one detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_google_ads_basic = OrderLineGoogleAdsBasicSerializer(required=False)
    """
    sub-serializer for google ads premium specific product data
    one detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_google_ads_premium = OrderLineGoogleAdsPremiumSerializer(required=False)

    """
    sub-serializer for display basic specific product data
    one detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_display_basic = OrderLineDisplayBasicSerializer(required=False)

    """
    sub-serializer for display premium specific product data
    one detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_display_premium = OrderLineDisplayPremiumSerializer(required=False)

    """
    sub-serializer for facebook specific product data
    one detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_facebook = OrderLineFacebookSerializer(required=False)

    """
    sub-serializer for in-app specific product data
    one detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_inapp = OrderLineInAppSerializer(required=False)

    """
    sub-serializer for listing specific product data
    one detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_listing = OrderLineListingSerializer(required=False)

    """
    sub-serializer for seo specific product data
    one detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_seo = OrderLineSeoSerializer(required=False)

    """
    sub-serializer for website specific product data
    easys detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_website = OrderLineWebsiteSerializer(required=False)

    """
    sub-serializer for landingpage specific product data
    easys detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_landingpage = OrderLineLandingpageSerializer(required=False)

    """
    sub-serializer for external website specific product data
    one detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_customer_website = OrderLineCustomerWebsiteSerializer(required=False)

    """
    sub-serializer for external email specific product data
    one detail dataset per order item, can be skipped if this detail is not meant for the item's product type
    """
    detail_email = OrderLineEmailSerializer(required=False)


class SellerSerializer(serializers.Serializer):
    """
    represents a selling user
    """

    """
    """
    easys_id = serializers.IntegerField(required=True)

    """
    """
    salesforce_id = serializers.CharField(min_length=15, max_length=18, required=True)

    """
    """
    sap_hr_id = serializers.CharField(max_length=20, required=True)


class SellerShareSerializer(serializers.Serializer):
    """
    represents the share a single seller holds on the whole sale
    overall sum of shares of all seller shares attached to an order must be exactly 100
    """

    """
    """
    share = serializers.IntegerField(min_value=1, max_value=100, required=True)

    """
    sub-serializer for seller specific data
    one seller per seller share
    """
    seller = SellerSerializer(many=False, required=True)


class OrderSerializer(serializers.Serializer):
    """
    represents the basic order details
    """

    """
    easys system id of the order

    """
    easys_id = serializers.IntegerField(required=True)

    """
    one system id of the account the order is subordinated_to

    """
    easys_account_id = serializers.IntegerField(required=True)

    """
    order revision, defines how often an order has been updated before the customer signed it

    """
    version = serializers.IntegerField(allow_null=True, required=False)

    """
    custom name of the order revision

    """
    version_name = serializers.CharField(max_length=50, allow_blank=True, required=False)

    """
    date of initial offer creation

    """
    date_created = serializers.DateTimeField(required=True)

    """
    date of offer lock

    """
    date_is_locked = serializers.DateTimeField(allow_null=True, required=False)

    """
    date of last offer modification

    """
    date_last_modified = serializers.DateTimeField(allow_null=True, required=False)

    """
    date of offer sent to the customer

    """
    date_sent_to_customer = serializers.DateTimeField(allow_null=True, required=False)

    """
    date when the customer signed the offer

    """
    date_signed = serializers.DateTimeField(required=True)

    """
    sub-serializer for seller shares
    multiple seller shares can be attached to a single order but their overall share must be exactly 100%
    """
    sellershares = SellerShareSerializer(many=True, required=True)


class FileSerializer(serializers.Serializer):
    """
    proof of offer file, e.g. pdf with signature, file scan, etc

    """
    filename = serializers.CharField()
    content = serializers.CharField()


class Serializer(serializers.Serializer):
    """
    base serializer that combines all order data
    """

    """
    sub-serializer for accounts
    """
    account = AccountSerializer(required=True)

    """
    sub-serializer for account locations
    """
    account_locations = AccountLocationSerializer(many=True, required=True)

    """
    sub-serializer for contacts
    """
    contacts = ContactSerializer(many=True, required=True)

    """
    sub-serializer for orders
    """
    orders = OrderSerializer(many=True, required=True)

    """
    sub-serializer for order lines
    """
    orderlines = OrderLineSerializer(many=True, required=True)

    """
    sub-serializer for offer proof files
    """
    files = FileSerializer(many=True, required=True)

    def validate(self, data):
        self.validate_easys_ids(data=data)
        self.validate_seller_shares(data=data)
        self.validate_productdetail_exists(data=data)
        self.validate_productfee_commissions(data=data)
        self.validate_deferred_payments(data=data)
        self.validate_website_and_landingpage_exists(data=data)
        return data

    def validate_productfee_commissions(self, data):
        for orderline in data['orderlines']:
            if orderline['product_type'] in [PRODUCT_TYPE_GOOGLE_ADS] and \
                    orderline['product_level'] in [PRODUCT_LEVEL_BASIC]:
                if orderline.get('commission') != Decimal('40'):
                    raise serializers.ValidationError('commission value for orderline {} is fixed to 40'.format(
                        orderline['easys_id']
                    ))

    def validate_deferred_payments(self, data):
        for orderline in data['orderlines']:
            if orderline.get('deferred_payment_sum', False) and not orderline.get('deferred_payment_months'):
                raise serializers.ValidationError('deferred payment months is required for orderline {}'.format(
                    orderline['easys_id']
                ))

    def validate_seller_shares(self, data):
        # verify that all accounts of orders are known
        for order in data['orders']:
            # verify that the sum of all seller shares is exactly 100
            sellershare_sum = 0
            for sellershare in order['sellershares']:
                sellershare_sum += sellershare['share']
            if sellershare_sum != 100:
                raise serializers.ValidationError(
                    'summed up seller shares of order {} are {}, must be exactly 100'.format(
                        order['easys_id'], sellershare_sum))

    def validate_productdetail_exists(self, data):
        for orderline in data['orderlines']:
            if orderline['product_type'] in PRODUCT_TYPE_ORDER_ATTRIBUTES_MAPPING:
                if not PRODUCT_TYPE_ORDER_ATTRIBUTES_MAPPING[orderline['product_type']].intersection(orderline.keys()):
                    raise serializers.ValidationError('orderline {} is missing the product detail data'.format(
                        orderline['easys_id']))

    def validate_website_and_landingpage_exists(self, data):
        # if one products has a its target urls chosen to be a HC website or landingpage,
        # validate that an order for it was delivered
        needs_website = False
        has_website = False
        needs_landingpage = False
        has_landingpage = False
        for orderline in data['orderlines']:
            if orderline['product_type'] in PRODUCT_TYPE_ORDER_ATTRIBUTES_MAPPING:
                detail_attribute = PRODUCT_TYPE_ORDER_ATTRIBUTES_MAPPING[orderline['product_type']].intersection(
                    orderline.keys()).pop()
                if orderline[detail_attribute].get('target_page_type') == NEW_WEBSITE:
                    needs_website = True
                if orderline[detail_attribute].get('target_page_type') == NEW_LANDINGPAGE:
                    needs_landingpage = True
                if orderline['product_type'] == PRODUCT_TYPE_LANDINGPAGE:
                    has_landingpage = True
                if orderline['product_type'] == PRODUCT_TYPE_WEBSITE:
                    has_website = True
        if needs_landingpage and not has_landingpage:
            raise serializers.ValidationError('orderline for Landingpage product has to be provided since it was a '
                                              'selected option in target_page_type in other product.')
        if needs_website and not has_website:
            raise serializers.ValidationError('orderline for Website product has to be provided since it was a '
                                              'selected option in target_page_type in other product.')

    def validate_easys_ids(self, data):
        # get ids to validate against
        account_id = data['account']['easys_id']
        account_location_ids = [d['easys_id'] for d in data['account_locations']]
        order_ids = [d['easys_id'] for d in data['orders']]

        # verify that all accounts on account locations are known
        for account_location in data['account_locations']:
            if account_location['easys_account_id'] != account_id:
                raise serializers.ValidationError('account id {} of account location {} is not known'.format(
                    account_location['easys_account_id'], account_location['easys_id']))

        # verify that all accounts of contacts are known
        for contact in data['contacts']:
            if contact['easys_account_id'] != account_id:
                raise serializers.ValidationError('account id {} of contact {} is not known'.format(
                    contact['easys_account_id'], contact['easys_id']))

        # verify that all accounts of orders are known
        for order in data['orders']:
            if order['easys_account_id'] != account_id:
                raise serializers.ValidationError('account id {} of order {} is not known'.format(
                    order['easys_account_id'], order['easys_id']))

        # verify that all orders and account locations of orderlines are known
        for orderline in data['orderlines']:
            if orderline['easys_order_id'] not in order_ids:
                raise serializers.ValidationError('order id {} of orderline {} is not known'.format(
                    orderline['easys_order_id'], orderline['easys_id']))
            if orderline['easys_account_location_id'] not in account_location_ids:
                raise serializers.ValidationError('account location id {} of orderline {} is not known'.format(
                    orderline['easys_account_location_id'], orderline['easys_id']))
