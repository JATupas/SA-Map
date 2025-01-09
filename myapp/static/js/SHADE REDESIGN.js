document.querySelectorAll('.tool-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
        const description = card.getAttribute('data-description');
        document.querySelector('.about-card p.default-text').innerText = description;
    });

    card.addEventListener('mouseleave', () => {
        document.querySelector('.about-card p.default-text').innerText = 'An effective strategy in evaluating seismic hazards plays a very crucial role in efforts at disaster risk reduction and management within a very seismically active country. Techniques available - be it probabilistic or deterministic-rely on extensive datasets with respect to attenuation models for ground motion, models for seismic sources, and earthquake catalogs. The SHADE Project developed a Python-based application that simplifies the computing and visualization of ground motion parameters in assessing seismic hazard in the Philippines.';
    });
});