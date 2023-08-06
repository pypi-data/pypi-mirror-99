CHANGELOG
=========

0.13.0 (2021-03-21)
-------------------

- Run tests with a test project against all modern Python + Django + CMS combinations
- Remove u-strings and dependency on six (backward-compatibility for Python 2)
- Fix ImportError on django CMS 3.8.0 (thanks @arnodeceuninck)

0.12.0 (2020-02-04)
-------------------

- Adjust migrations for Django 2+ (thanks @macolo)
- Fix some code smell in JS reported by Codacy
- Allow jshint to run locally (via tox)

0.11.0 (2019-05-08)
-------------------

- Add aldryn_config.py to make plugin visible on Divio marketplace
- Reformat code (inital migrations, models, forms, templatetags)

0.10.0 (2019-01-30)
-------------------

- Convert float to string before evaluating (thanks @mireq)

0.9.0 (2019-01-12)
------------------

- Don't show map title when it's blank (thanks @adrien-delhorme)

0.8.0 (2018-03-04)
------------------

- Fix float rounding error for map coordinates on German sites (which use
  a colon instead of a period)
- Configure HERE WeGo to use HTTPS by default

0.7.0 (2016-09-14)
------------------

- Implement ViaMichelin provider

0.6.0 (2016-09-02)
------------------

- Allow to display or hide layers control and scale bar
- Implement HERE WeGo provider
- Bugfix: Allow keyboard navigation (Mapbox)
- Run static code analysis for all supported Python versions
- Implement Bing Maps provider

0.5.0 (2016-09-01)
------------------

- Fork ``djangocms-googlemap`` plugin, remove legacy burden
- Refactor template structure for multi-provider support
- Remove routing options from plugin UI (plan: re-implement on the map)
- Reorganice plugin UI to avoid excessive scrolling
- Add settings (API keys) for Google Maps and all future providers
- Implement Mapbox provider
- Add stubs for Bing, HERE, ViaMichelin

before 0.5.0
------------

- See change log of Divio's djangocms-googlemap_.

.. _djangocms-googlemap: https://github.com/divio/djangocms-googlemap/blob/master/CHANGELOG.rst
