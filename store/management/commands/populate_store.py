from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Popola il database con account demo, strumenti musicali e accessori'

    def handle(self, *args, **kwargs):
        # 1. CREAZIONE UTENTI DEMO
        User = get_user_model()

        self.stdout.write(self.style.WARNING('Creazione account demo in corso...'))

        # Creazione Manager / Admin
        if not User.objects.filter(username='admin_demo').exists():
            admin_user = User.objects.create_superuser(
                username='admin_demo',
                email='admin@mikusoundvault.com',
                password='admin12345'
            )
            admin_user.role = 'manager'
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Account Manager "admin_demo" creato con password "admin12345".'))
        else:
            self.stdout.write('Account "admin_demo" già esistente.')

        # Creazione Cliente Standard
        if not User.objects.filter(username='user_demo').exists():
            standard_user = User.objects.create_user(
                username='user_demo',
                email='user@mikusoundvault.com',
                password='user12345'
            )
            standard_user.role = 'customer'
            standard_user.save()
            self.stdout.write(self.style.SUCCESS('Account Cliente "user_demo" creato con password "user12345".'))
        else:
            self.stdout.write('Account "user_demo" già esistente.')

        self.stdout.write(self.style.WARNING('-' * 30))

        # 2. CREAZIONE CATEGORIE E PRODOTTI
        data = {
            'Chitarre': [
                ('Chitarra Elettrica "Miku Blue"', 850.00,
                 '🎸 Una chitarra elettrica dal colore teal vibrante. Suono cristallino.'),
                ('Chitarra Acustica "Woods"', 450.00, '🎸 Legno di mogano per un suono caldo e profondo.'),
                ('Basso Elettrico "Deep Bass"', 600.00, '🎸 4 corde, perfetto per il funk e il rock.'),
                ('Chitarra Semi-Acustica Jazz', 980.00, '🎸 Eleganza e calore per i tuoi fraseggi jazz.'),
            ],
            'Tastiere e Piano': [
                ('Sintetizzatore Digital Voice', 1200.00, '🎹 Synth polifonico con oltre 500 preset elettronici.'),
                ('Piano Digitale "Grand"', 2100.00, '🎹 Tasti pesati e campionamento di un vero pianoforte a coda.'),
                ('Midi Controller 49 Tasti', 150.00, '🎹 Compatto e pronto per la tua DAW.'),
                ('Keytar "Stage Star"', 350.00, '🎹 Per chi vuole dominare il palco con stile.'),
            ],
            'Batteria e Percussioni': [
                ('Batteria Acustica 5 Pezzi', 950.00, '🥁 Kit completo di piatti e supporti.'),
                ('Batteria Elettronica "Silent"', 700.00, '🥁 Perfetta per studiare in appartamento senza disturbare.'),
                ('Cajon in Betulla', 120.00, '🥁 Percussione acustica versatile per sessioni unplugged.'),
                ('Set Piatti Professionali', 400.00, '🥁 Ride, Crash e Hi-Hat di alta qualità.'),
            ],
            'Accessori': [
                ('Cavo Jack 3m "Gold"', 25.00, '🔌 Connettori placcati oro per la massima fedeltà.'),
                ('Set di Plettri (10 pz)', 10.00, '🎼 Vari spessori per ogni stile.'),
                ('Custodia Rigida Universale', 80.00, '🎒 Protezione massima per il tuo strumento.'),
                ('Supporto per Tastiera', 45.00, '🎹 Robusto e regolabile in altezza.'),
                ('Accordatore Cromatico a Clip', 15.00, '🎸 Precisione massima per ogni corda.'),
                ('Cuffie Monitor Studio', 120.00, '🎧 Risposta piatta per il mixing perfetto.'),
            ]
        }

        self.stdout.write(self.style.WARNING('Popolamento catalogo in corso...'))

        for cat_name, products in data.items():
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': slugify(cat_name), 'description': f'Tutti i prodotti della categoria {cat_name}'}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoria "{cat_name}" creata.'))

            for name, price, desc in products:
                product, p_created = Product.objects.get_or_create(
                    name=name,
                    category=category,
                    defaults={
                        'slug': slugify(name),
                        'price': price,
                        'description': desc,
                        'stock': 10,
                        'available': True
                    }
                )
                if p_created:
                    self.stdout.write(self.style.SUCCESS(f'Prodotto "{name}" creato.'))

        self.stdout.write(
            self.style.SUCCESS('\n✅ Popolamento completato con successo! Il database è pronto per i test.'))