from django.core.management.base import BaseCommand

from measurements.sources.cmems_wms import CMEMSWmsDataSource
from measurements.models import SourceType
from measurements.utils import get_serie, load_serie


class Command(BaseCommand):
    help = "Command to import CMEMS WMS data."

    def handle(self, *args, **options):
        ps = SourceType.objects.get(code='cmems_wms')
        for station in ps.station_set.filter(status='active'):
            self.stdout.write("Loading DataSource/Station {} ... ".format(station))
            apiclient = CMEMSWmsDataSource(station.uri)

            self.stdout.write("\tLooking for registered layers/parameters ...")
            for pm in station.parametermapping_set.all():
                parameter = pm.parameter
                layer = pm.source_parameter_label
                self.stdout.write("\tLooking for registered series ...")
                for series in station.serie_set.filter(parameter=parameter).all():
                    location = series.location
                    # print(series)
                    self.stdout.write(
                        "\tLoading series {}. Layer {}. Location {} ... ".format(series.id, layer, location),
                        ending=''
                    )
                    point = [location.geo.x, location.geo.y]

                    df = apiclient.get_df(layer, point, timedelta=10) - 273.15
                    if df.shape[0] > 0:
                        load_serie(df['value'].copy(), series.id)
                        self.stdout.write("[OK]")
                    else:
                        self.stdout.write("[FAILED]")
