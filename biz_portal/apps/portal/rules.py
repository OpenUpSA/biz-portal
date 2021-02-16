"""
We use this for object-level authorisation.

Don't implement something here that can be fully handled by built-in
Django permissions
"""

import logging

import rules

logger = logging.getLogger(__name__)


@rules.predicate
def is_business_muni_admin(user, business):
    logger.debug(
        f"Predicate {is_business_muni_admin.__name__} user={user} business={business}"
    )

    if not user.is_staff:
        return False

    if business is None:
        return False

    return user.municipality_set.filter(pk=business.region.municipality.pk).exists()


@rules.predicate
def is_muni_admin(user):
    """
    Is an admin of SOME municipality
    """
    logger.debug(f"Predicate {is_muni_admin.__name__}")
    return user.is_staff and user.municipality_set.exists()

# This rule can't restrict addition of business to the munis the user can
# admin so we rely on that being enforced in the ModelAdmin.
rules.add_perm("portal.add_business", is_muni_admin)
rules.add_perm("portal.change_business", is_business_muni_admin)
rules.add_perm("portal.delete_business", is_business_muni_admin)
rules.add_perm("portal.add_businessmembership", is_business_muni_admin)
rules.add_perm(
    "portal.change_businessmembership", is_business_muni_admin
)
rules.add_perm(
    "portal.delete_businessmembership", is_business_muni_admin
)
