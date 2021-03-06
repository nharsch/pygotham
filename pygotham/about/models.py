"""About models."""

from slugify import slugify
from sqlalchemy_utils import observes

from pygotham.core import db
from pygotham.events.query import EventQuery

__all__ = ('AboutPage',)


class AboutPage(db.Model):
    """About page."""

    __tablename__ = 'about_pages'
    query_class = EventQuery

    id = db.Column(db.Integer, primary_key=True)
    # TODO: validate that the navbar_section / slug combination do not conflict
    # with an existing generated blueprint view route
    navbar_section = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    event_id = db.Column(
        db.Integer, db.ForeignKey('events.id'), nullable=False,
    )
    event = db.relationship(
        'Event', backref=db.backref('about_pages', lazy='dynamic'),
    )

    __table_args__ = (
        db.UniqueConstraint(
            'navbar_section', 'slug', 'event_id',
            name='ix_about_pages_navbar_section_slug_event_id',
        ),
    )

    def __str__(self):
        """Return a printable representation."""
        return self.title

    @observes('title')
    def _create_slug(self, title):
        """Create the slug for the page."""
        if not self.slug:
            self.slug = slugify(self.title)

    @property
    def rst_document(self):
        """Return the full reST document, including the title.

        The page's title was be used as the document heading, causing
        any headings defined in the page's content to be used as
        subheadings. To cut down on potential collisions, ``#`` symbols
        will be placed on the lines before and after the title.
        """
        lines = ('{divider}', '{page.title}', '{divider}', '{page.content}')
        return '\n'.join(lines).format(
            divider='#' * len(self.title), page=self)
