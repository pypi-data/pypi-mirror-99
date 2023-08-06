# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

from . import Reader


class CSVReader(Reader):
    def to_pandas(self, **kwargs):
        import pandas

        options = {}
        options.update(self.source.read_csv_options())
        options.update(kwargs)

        return pandas.read_csv(self.path, **options)
