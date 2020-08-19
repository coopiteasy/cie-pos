This module fix the issue on picking when there is two lines on
the pos order for the same product, with one of lines with a 0 quantity.
The lines with quantity set to 0 are removed before the pos order is
processed to avoid such issue.
