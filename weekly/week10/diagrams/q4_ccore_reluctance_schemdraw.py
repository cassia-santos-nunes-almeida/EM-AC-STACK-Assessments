"""Q4: C-Core — Reluctance equivalent circuit."""
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing(file='diagrams/week10/q4_ccore_reluctance.svg') as d:
    d.config(unit=3.5, fontsize=14, font='sans-serif')

    # MMF source (modelled as voltage source in reluctance analogy)
    source = d.add(elm.SourceV().up().label('$NI$\n(MMF)', loc='top', ofst=0.15))

    # Top rail
    d += elm.Line().right().length(5).at(source.end)

    # Core reluctance (going down)
    Rcore = d.add(elm.Resistor().down().label(
        '$\\mathcal{R}_{\\mathrm{core}} = \\dfrac{\\ell_c}{\\mu_r \\mu_0 A_c}$',
        loc='bottom', ofst=0.15))

    # Air gap reluctance (going down)
    Rgap = d.add(elm.Resistor().down().label(
        '$\\mathcal{R}_{\\mathrm{gap}} = \\dfrac{\\ell_g}{\\mu_0 A_c}$',
        loc='bottom', ofst=0.15))

    # Bottom return
    d += elm.Line().left().tox(source.start)
    d += elm.Line().up().toy(source.start)

    # Flux arrow (analogous to current)
    d += elm.CurrentLabelInline(direction='in').at(Rcore).label('$\\Phi$')
