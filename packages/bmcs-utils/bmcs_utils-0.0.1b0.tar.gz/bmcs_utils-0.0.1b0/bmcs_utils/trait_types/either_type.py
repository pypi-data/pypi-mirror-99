#-------------------------------------------------------------------------
#
# Copyright (c) 2009, IMB, RWTH Aachen.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in simvisage/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.simvisage.com/licenses/BSD.txt
#
# Thanks for using Simvisage open source!
#
# Created on Aug 7, 2009 by: rchx

from traits.api import TraitType, TraitError
from bmcs_utils.editors import EitherTypeEditor

import traits.api as tr

class EitherType(TraitType):
    """Polymorphic instance - can accommodate the values
    of specified classes. Instances of the classes are created upon key assignement
    Unused instances are kept in cache."""
    editor_factory = EitherTypeEditor

    is_mapped = True

    def __init__(self, options = [], **metadata):
        # validate that these are trait types
        self.options_dict = {key: value for key, value in options}
        metadata.update({'options': options})
        super(EitherType, self).__init__(**metadata)
        self.map = {}

    def mapped_value(self, key):
        """ Get the mapped value for a value. """
        return self.map.get(key,None)

    def post_setattr(self, object, name, key):
        # check if the last instance of the klass has been
        # registered earlier in the trait history
        new_value = self.mapped_value(key)
        if new_value == None:
            klass = self.options_dict.get(key, None)
            new_value = klass()
            self.map[key] = new_value
        # set the shadow attribute
        # editor uses it to asociate the value with the option.
        setattr(object, name + "_", new_value)

    def validate(self, object, name, key):
        ''' Set the trait value '''
        klass = self.options_dict.get(key,None)
        if klass == None:
            raise TraitError('type %s not in the type scope' % klass)
        return key

    def get_default_value(self):
        '''Take the first class to construct the value'''
        key, _ = self.options[0]
        return (0, key)
