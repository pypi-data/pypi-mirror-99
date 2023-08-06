from utilities.choices import ChoiceSet


class VirtualCircuitStatusChoices(ChoiceSet):
    """List of possible status for a Virtual Circuit."""

    STATUS_PENDING_CONFIGURATION = 'pending-configuration'
    STATUS_CONFIGURED = 'configured'
    STATUS_CONFIGURATION_ERROR = 'configuration-error'
    STATUS_PENDING_DEACTIVATION = 'pending-deactivation'
    STATUS_DEACTIVATED = 'deactivated'

    CHOICES = (
        (STATUS_PENDING_CONFIGURATION, 'Ожидает'),
        (STATUS_CONFIGURED, 'Настроен'),
        (STATUS_CONFIGURATION_ERROR, 'Ошибка'),
        (STATUS_PENDING_DEACTIVATION, 'В ожидании отключения'),
        (STATUS_DEACTIVATED, 'Отключен'),
    )
