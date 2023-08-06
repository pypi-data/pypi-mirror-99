
Installing
----------

.. code-block:: bash

  pip install newsworthy_slides


Using
-----

This library has one main function: :code:`slides_from_xml()` which lets you generate and slides from a custom HTML structure (described below).

Basic usage:

.. code-block:: python

  from newsworthy_slides import slides_from_xml

  slides_xml = """
  <slide layout="Title and content">
    <placeholder type="text">
      Hello world!
    </placeholder>
  </slide>
  """

  # Generate to new, empty presentation
  pres = slides_from_xml(slides_xml)

  # Generate to existing presentation
  pres = slides_from_xml(slides_xml, "path/to/my_base_slides.pptx")

  # pres is an instance of pptx.Presentation and can be saved easily:
  pres.save('my_presentation.pptx')



The XML structure
-----------------


Slides
~~~~~~

A slide must always have a :code:`layout` attribute referring to the name of a slide layout.

.. code-block:: XML

  <slide layout="Title and content">
  </slide>

A slide `may` have :code:`position` attribute which defines where in the presentation the slide is to be added.

A slide consists of a number of placeholders.

.. code-block:: XML

  <slide layout="Title and content">
    <placeholder type="text">
      Hello world!
    </placeholder>
  </slide>

Each placeholder must have  a :code:`type` attribute, which can be either :code:`text`, :code:`image`, :code:`table`. The :code:`type` attribute defines how the content of the tag is to be interpreted.

The placeholders may also have a :code:`name` attribute. This attribute should refer to a placeholder name in the slide layout.

.. code-block:: XML

  <slide layout="Title and content">
    <placeholder type="text" name="Text Placeholder 1">Hello</placeholder>
    <placeholder type="text" name="Text Placeholder 2">World!</placeholder>
  </slide>

If no placeholder name is defined the placeholders will be positioned in order.

.. code-block:: XML

  <slide layout="Title and content">
    <placeholder type="text">First placeholder</placeholder>
    <placeholder type="text">Second placeholder</placeholder>
  </slide>


The different placeholders types are defined below.

Text placeholders
~~~~~~~~~~~~~~~~~

Text placeholders may contain plain text or basic html. :code:`<p>` and :code:`<li>` tags are interpreted as paragraphs.

.. code-block:: XML

  <placeholder type="text">
    Hello world!
  </placeholder>

  <placeholder type="text">
    <p>Hello Earth!</p>
    <p>Hello Mars!</p>
  </placeholder>

  <placeholder type="text" auto-size="text-to-fit-shape">
    <li>Hello Earth!</li>
    <li>Hello Mars!</li>
    <li>Hello Jupiter!</li>
    <li>Hello Saturn!</li>
    <li>Hello Uranus!</li>
  </placeholder>

:code:`<strong>`, :code:`<i>`/`<em>` and :code:`<a>` tags may be used for inline formating and linking.

The :code:`auto-size` attribute may be set to autosize either the text (:code:`text-to-fit-shape`) or the shape (:code:`shape-to-fit-text`).

.. code-block:: XML

  <placeholder type="text">
    Hello <strong>world</strong>. Considering a <a href="http://outer.space">Mars</a>?
  </placeholder>


Image placeholders
~~~~~~~~~~~~~~~~~~

An image placeholder recognizes :code:`<img>` tags and picks up the path (or url) to the image from the :code:`src` attribute.

.. code-block:: XML

  <placeholder type="image" vertical-alignment="top>
    <img src="path/to/image.png">
  </placeholder>

Use attributes :code:`vertical-alignment` (or :code:`va`) and :code:`horizontal-alignment` (or :code:`ha`) for positioning.

Note that the placeholder explicitly has to be either a picture or an object placeholder. This has to be set manually in Powerpoint. At the moment of writing Google Slides does not support picture placeholders (neither does Libre Office). 

Table placeholders
~~~~~~~~~~~~~~~~~~

A table placeholder should contain an html table. All :code:`<tr>` tags are parsed as rows. :code:`<td>` and :code:`<th>` tags are parsed as cells. The cells may contain same basic text formatting as paragraphs (`<strong>` for bold, :code:`<i>` for italic etc).

Cells with :code:`class="value"` are interpreted as numbers and right-aligned.

`<thead>` and :code:`<tbody>` may be present, but does not bring any meaning. :code:`<caption>` is _not_ parsed.

.. code-block:: XML

  <placeholder type="table">
    <table>
        <tr>
          <td>Country</td>
          <td>Happiness</td>
        </tr>
        <tr>
          <td>Finland</td>
          <td class="value">9.5</td>
        </tr>
        <tr>
          <td>Sweden</td>
          <td class="value">8.5</td>
        </tr>
    </table>
  </placeholder>

Notes
~~~~~

A slide may contain :code:`<notes>` tag containing slide notes. The content will be parsed as text just as regular text placeholders.

.. code-block:: XML

  <notes>
    <li>Here is an important thing to keep in mind!</<li>
  </notes>


Presentation metadata
~~~~~~~~~~~~~~~~~~~~~

Presentation level metadata such as title, author and comments may be defined as attributes of a :code:`<presentation>` tag. Available properties equals the `core properties of the pptx library <https://python-pptx.readthedocs.io/en/latest/api/presentation.html#pptx.opc.coreprops.CoreProperties>`_.

.. code-block:: XML

  <presentation title="My Report" author="John Smith" created="2020-01-01">
  </presentation>

Developing
----------

To run tests:

.. code-block:: bash

  python3 -m pytest test

Deployment
----------

To deploy a new version to PyPi:

1. Update Changelog below.
2. Update :code:`version.py`
3. Build: :code:`python3 setup.py sdist bdist_wheel`
4. Upload: :code:`python3 -m twine upload dist/newsworthy_slides-X.Y.X*`

...assuming you have Twine installed (`pip install twine`) and configured.

Changelog
---------

- 1.6.0

  - New feature: Notes

- 1.5.0

  - Enable alignment of images.

- 1.4.0

  - Enable autosizing of text.

- 1.3.0

  - Enable insertion of image to general purpose object placeholders.

- 1.2.0

  - Adds ability to parse presentation level metadata.

- 1.1.1

  - Bug fix: Handle negative rotation.

- 1.1.0

  - Makes it possible to rotate images.

- 1.0.2

  - Fixes ordering bug in table

- 1.0.1

  - Add custom exception if image is missing

- 1.0.0

  - First version
