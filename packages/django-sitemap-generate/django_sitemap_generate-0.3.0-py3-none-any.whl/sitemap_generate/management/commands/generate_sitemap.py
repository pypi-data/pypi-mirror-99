from django.conf import settings
from django.core.management import BaseCommand
from django.utils.module_loading import import_string

from sitemap_generate.generator import SitemapGenerator


class Command(BaseCommand):
    help = "generate sitemap xml files"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('sitemap', type=str, nargs='?')

    def handle(self, *args, **options):
        generator = SitemapGenerator()
        generator.generate(options.get('sitemap'))
