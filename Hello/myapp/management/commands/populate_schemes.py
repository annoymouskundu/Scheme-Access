import os
from django.core.management.base import BaseCommand
from myapp.models import GovernmentScheme  # Adjust import based on your app structure

class Command(BaseCommand):
    help = 'Populate government schemes from a file'

    def handle(self, *args, **kwargs):
        # Path to your schemes folder (assuming all text files are there)
        schemes_folder_path = r'C:\Users\ROZY\Desktop\GitHub\Scheme-Access\Hello\schemes'
        
        try:
            for filename in os.listdir(schemes_folder_path):
                if filename.endswith('.txt'):
                    file_path = os.path.join(schemes_folder_path, filename)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        
                        # Split content into individual schemes (assuming each scheme is separated by a specific delimiter)
                        scheme_entries = content.split('\n\n')  # Adjust based on how schemes are separated

                        for entry in scheme_entries:
                            lines = entry.strip().split('\n')
                            if len(lines) < 3:
                                continue  # Skip entries that don't have enough information

                            scheme_name = lines[0].replace('Scheme Name:', '').strip()
                            eligibility_criteria = lines[1].replace('Eligibility Criteria:', '').strip()
                            benefits = lines[2].replace('Benefits:', '').strip()

                            # Create and save the GovernmentScheme instance
                            GovernmentScheme.objects.create(
                                name=scheme_name,
                                eligibility_criteria={'details': eligibility_criteria},  # Store as JSON if needed
                                benefits=benefits
                            )

            self.stdout.write(self.style.SUCCESS('Successfully populated government schemes from the files'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('The specified schemes folder was not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
