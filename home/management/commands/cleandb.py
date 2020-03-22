from django.core.management.base import BaseCommand, CommandError
from users.models import Invite

class Command(BaseCommand):
    help = 'Deletes extraneous rows from database'

    def handle(self, *args, **kwargs):
        # collect expired invites
        expired = [x for x in Invite.objects.filter(user=None) if x.expired]

        # return success if empty
        if expired:
            len_expired = len(expired)
            self.stdout.write('{} invite{} to delete.'.format(len_expired, '' if len_expired == 1 else 's'))
        else:
            self.stdout.write(self.style.SUCCESS('Command successful. No invites to delete.'))
            return

        # table member widths
        width_id = max((len(str(x.id)) for x in expired)) + 2
        width_code = 34
        width_expiry = 18

        # top line of table
        self.stdout.write('┌{}┬{}┬{}┐'.format('─' * width_id, '─' * width_code, '─' * width_expiry))

        # table header
        self.stdout.write('│{:^{width_id}}│{:^{width_code}}│{:^{width_expiry}}│'.format('ID', 'Code', 'Date Expired', width_id=width_id, width_code=width_code, width_expiry=width_expiry))

        # header/body divider
        self.stdout.write('╞{}╪{}╪{}╡'.format('═' * width_id, '═' * width_code, '═' * width_expiry))

        # body
        for x in expired:
            self.stdout.write('│{:^{width_id}}│{:^{width_code}}│{:^{width_expiry}}│'.format(x.id, x.code, x.expiry_date.strftime('%m/%d/%Y %H:%M'), width_id=width_id, width_code=width_code, width_expiry=width_expiry))

        # bottom line of table
        self.stdout.write('└{}┴{}┴{}┘'.format('─' * width_id, '─' * width_code, '─' * width_expiry))

        # actual deletion
        expired.delete()

        # success message
        self.stdout.write(self.style.SUCCESS('Successfully deleted {} invite{}.'.format(len_expired, '' if len_expired == 1 else 's')))
