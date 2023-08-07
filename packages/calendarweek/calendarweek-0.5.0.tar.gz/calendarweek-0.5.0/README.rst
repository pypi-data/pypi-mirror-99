python-calendarweek
===================

python-calendarweek provides a CalendarWeek dataclass for representing one
week in a year, and utility functions to work with it in pure Python or
Django.


Usage
-----

The `CalendarWeek` object
~~~~~~~~~~~~~~~~~~~~~~~~~

The main interface is the `CalendarWeek` object. The following example shows its
interface.

.. code-block:: python

   from datetime import date
   from calendarweek import CalendarWeek

   # Create an object for the third week in 2012
   week = CalendarWeek(year=2012, week=3)

   # Get the current week (or the week for any date)
   week = CalendarWeek.from_date(date.today())

   # Short-hand for the current week
   week = CalendarWeek()

   # Get all weeks within a date range
   start = date(2012, 3, 18)
   end = date(2012, 4, 19)
   weeks = CalendarWeek.weeks_within(start, end)

   # Get the last week of a year
   week = CalendarWeek.get_last_week_of_year(2012)

   # Get the Wednesday of the selected week (or any weekday)
   day = week[3]

   # Check whether a day is within a week
   is_contained = day in week

   # Get the week five weeks later
   week = week + 5

   # Additionally, all comparison operators are implemented


Django utilities
~~~~~~~~~~~~~~~~

Some utilities for Django are contained in the `calendarweek.django` module:

- `i18n_day_names` — Returns a tuple of localised day names
- `i18n_day_abbrs` — Returns a tuple of abbreviated, localised day names
- `i18n_month_names` — Returns a tuple of localised month names
- `i18n_month_abbrs` — Returns a tuple of abbreviated, localised month names
- All the above for suffixed with `_choices` to get a list of tuples ready for a model
  or form field's `choices`
- `i18n_js` — A view returning the above as JSON ready to be consumed by a frontend
