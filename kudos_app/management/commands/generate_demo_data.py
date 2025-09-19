from django.core.management.base import BaseCommand
from django.db import transaction
import random
from datetime import datetime, timedelta
from kudos_app.models import Organization, User, Kudo


class Command(BaseCommand):
    help = 'Generate demo data for the Kudos application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before generating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Kudo.objects.all().delete()
            User.objects.all().delete()
            Organization.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        with transaction.atomic():
            self.create_organizations()
            self.create_users()
            self.create_kudos()

        self.stdout.write(self.style.SUCCESS('Demo data generated successfully!'))

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
        
        # Predefined messages for more realistic demo data
        messages = [
            "Great job on the project presentation! Your attention to detail really showed.",
            "Thanks for helping me debug that tricky issue. You saved the day!",
            "Your creative solution to the performance problem was brilliant.",
            "Appreciate you staying late to help the team meet the deadline.",
            "Your positive attitude during the stressful week kept everyone motivated.",
            "Excellent work on the user interface design. It looks amazing!",
            "Thank you for mentoring the new team member. Your guidance was invaluable.",
            "Your thorough code review caught several important issues. Great work!",
            "I loved your innovative approach to solving that complex problem.",
            "Thanks for organizing the team lunch. It was great for team bonding!",
            "Your documentation is always so clear and helpful. Thank you!",
            "Great job facilitating that difficult client meeting.",
            "Your quick response to the production issue prevented major downtime.",
            "Thanks for sharing your knowledge during the tech talk. Very insightful!",
            "Your collaboration skills make every project better.",
        ]

        # Create some kudos for the past few weeks to show realistic data
        current_date = datetime.now().date()
        
        # Create kudos for this week (some users should have remaining kudos)
        self.create_kudos_for_period(current_date - timedelta(days=current_date.weekday()), 
                                   current_date, messages, 0.4)  # 40% chance per user pair
        
        # Create kudos for last week
        last_week_start = current_date - timedelta(days=current_date.weekday() + 7)
        last_week_end = current_date - timedelta(days=current_date.weekday() + 1)
        self.create_kudos_for_period(last_week_start, last_week_end, messages, 0.7)  # 70% chance
        
        # Create kudos for the week before
        two_weeks_ago_start = current_date - timedelta(days=current_date.weekday() + 14)
        two_weeks_ago_end = current_date - timedelta(days=current_date.weekday() + 8)
        self.create_kudos_for_period(two_weeks_ago_start, two_weeks_ago_end, messages, 0.6)  # 60% chance

    def create_kudos_for_period(self, start_date, end_date, messages, probability):
        """Create kudos for a specific time period"""
        kudos_created = 0
        
        # Group users by organization
        users_by_org = {}
        for user in self.users:
            org_id = user.organization.id
            if org_id not in users_by_org:
                users_by_org[org_id] = []
            users_by_org[org_id].append(user)
        
        # Create kudos within each organization
        for org_users in users_by_org.values():
            for sender in org_users:
                # Each user can give up to 3 kudos per week
                kudos_to_give = random.randint(0, 3)
                
                # Randomly decide if this user gives kudos this week
                if random.random() > probability:
                    continue
                
                # Select random receivers from the same organization (excluding sender)
                possible_receivers = [u for u in org_users if u != sender]
                if not possible_receivers:
                    continue
                
                receivers = random.sample(
                    possible_receivers, 
                    min(kudos_to_give, len(possible_receivers))
                )
                
                for receiver in receivers:
                    # Create kudo with random date in the period
                    days_diff = (end_date - start_date).days
                    if days_diff > 0:
                        random_date = start_date + timedelta(days=random.randint(0, days_diff))
                        kudo_datetime = datetime.combine(
                            random_date, 
                            datetime.now().time().replace(
                                hour=random.randint(9, 17),
                                minute=random.randint(0, 59)
                            )
                        )
                    else:
                        kudo_datetime = datetime.combine(start_date, datetime.now().time())
                    
                    kudo = Kudo.objects.create(
                        sender=sender,
                        receiver=receiver,
                        message=random.choice(messages),
                        created_at=kudo_datetime
                    )
                    kudos_created += 1
        
        period_name = f"{start_date} to {end_date}"
        self.stdout.write(f'  Created {kudos_created} kudos for period: {period_name}')

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
