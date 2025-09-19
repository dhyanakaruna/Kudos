from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime, timedelta
from kudos_app.models import Organization, User, Kudo


class Command(BaseCommand):
    help = 'Generate demo data for the Kudos application (hardcoded, no randomness)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data',
        )
        parser.add_argument(
            '--clear-only',
            action='store_true',
            help='Clear existing data without generating new data',
        )

    def handle(self, *args, **options):
        if options['clear'] or options['clear_only']:
            self.stdout.write('Clearing existing data...')
            Kudo.objects.all().delete()
            User.objects.all().delete()
            Organization.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        # If --clear-only is specified, don't generate new data
        if options['clear_only']:
            return

        with transaction.atomic():
            self.create_organizations()
            self.create_users()
            self.create_kudos()

        self.stdout.write(self.style.SUCCESS('Demo data generated successfully!'))
        self.print_summary()

    def create_organizations(self):
        self.stdout.write('Creating organizations...')
        
        organizations_data = [
            'Company A',
            'Company B', 
            'Company C',
            'Company D'
        ]

        self.organizations = []
        for org_name in organizations_data:
            org, created = Organization.objects.get_or_create(name=org_name)
            self.organizations.append(org)
            if created:
                self.stdout.write(f'  Created organization: {org_name}')

    def create_users(self):
        self.stdout.write('Creating users...')
        
        users_data = [
            # Company A
            ('user1', 'user1@companya.com', 0),
            ('user2', 'user2@companya.com', 0),
            ('user3', 'user3@companya.com', 0),
            ('user4', 'user4@companya.com', 0),
            ('user5', 'user5@companya.com', 0),
            
            # Company B
            ('user6', 'user6@companyb.com', 1),
            ('user7', 'user7@companyb.com', 1),
            ('user8', 'user8@companyb.com', 1),
            ('user9', 'user9@companyb.com', 1),
            
            # Company C
            ('user10', 'user10@companyc.com', 2),
            ('user11', 'user11@companyc.com', 2),
            ('user12', 'user12@companyc.com', 2),
            
            # Company D
            ('user13', 'user13@companyd.com', 3),
            ('user14', 'user14@companyd.com', 3),
            ('user15', 'user15@companyd.com', 3),
        ]

        self.users = []
        for username, email, org_index in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'organization': self.organizations[org_index]
                }
            )
            self.users.append(user)
            if created:
                self.stdout.write(f'  Created user: {username} ({self.organizations[org_index].name})')

    def create_kudos(self):
        self.stdout.write('Creating kudos...')

        # Predefined static messages
        messages = [
            "Great teamwork!",
            "Thanks for your help!",
            "Awesome contribution!",
            "Really appreciated your effort!",
            "Fantastic work on the project!",
        ]

        # Current week range
        current_date = datetime.now().date()
        start_date = current_date - timedelta(days=current_date.weekday())

        kudos_created = 0

        # Group users by organization
        users_by_org = {}
        for user in self.users:
            org_id = user.organization.id
            if org_id not in users_by_org:
                users_by_org[org_id] = []
            users_by_org[org_id].append(user)

        # Each user gives exactly 1 kudo (so 2 remain)
        for org_users in users_by_org.values():
            for i, sender in enumerate(org_users):
                receiver = org_users[(i + 1) % len(org_users)]  # round-robin
                message = messages[i % len(messages)]

                # Fixed date: Wednesday 10 AM of current week
                kudo_date = start_date + timedelta(days=2)
                kudo_time = datetime.combine(kudo_date, datetime.min.time()).replace(hour=10, minute=0)

                Kudo.objects.create(
                    sender=sender,
                    receiver=receiver,
                    message=message,
                    created_at=kudo_time
                )
                kudos_created += 1
                self.stdout.write(
                    f'  Created kudo: {sender.username} -> {receiver.username} ({message})'
                )

        self.stdout.write(f'  Created {kudos_created} kudos (hardcoded)')
        self.stdout.write(f'  Ensured each user has at least 2 kudos remaining')

    def print_summary(self):
        """Print a summary of created data"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write('DEMO DATA SUMMARY')
        self.stdout.write('='*50)
        
        for org in Organization.objects.all():
            users_count = User.objects.filter(organization=org).count()
            kudos_count = Kudo.objects.filter(sender__organization=org).count()
            self.stdout.write(f'\n{org.name}:')
            self.stdout.write(f'  Users: {users_count}')
            self.stdout.write(f'  Kudos given: {kudos_count}')
            
            # Show remaining kudos for each user
            for user in User.objects.filter(organization=org):
                remaining = user.get_remaining_kudos()
                self.stdout.write(f'    {user.username}: {remaining} kudos remaining this week')
