import itertools

import numpy as np
import pytest

from Starfish.transforms import (
    instrumental_broaden,
    rotational_broaden,
    resample,
    doppler_shift,
    chebyshev_correct,
    extinct,
    rescale,
    renorm,
)
from Starfish.utils import calculate_dv, create_log_lam_grid


@pytest.fixture
def benchmark_data(request):
    wave = np.linspace(1e4, 5e4, request.param)
    flux = np.random.randn(request.param) + 1e10
    yield wave, flux


class TestInstrumentalBroaden:
    @pytest.mark.parametrize("fwhm", [-20, -1.00, -np.finfo(np.float64).tiny])
    def test_bad_fwhm(self, mock_data, fwhm):
        with pytest.raises(ValueError):
            instrumental_broaden(*mock_data, fwhm)

    def test_0_fwhm(self, mock_data):
        flux = instrumental_broaden(*mock_data, 0)
        np.testing.assert_allclose(flux, mock_data[1])

    def test_inst_broadening_fwhm(self, mock_data):
        flux = instrumental_broaden(*mock_data, 400)
        assert not np.allclose(mock_data[1], flux)

    def test_many_fluxes(self, mock_data):
        flux_stack = np.tile(mock_data[1], (4, 1))
        fluxes = instrumental_broaden(mock_data[0], flux_stack, 400)
        assert fluxes.shape == flux_stack.shape
        assert not np.allclose(fluxes, flux_stack)

    @pytest.mark.parametrize(
        "benchmark_data", [100, 500, 1000, 5000, 10000], indirect=True
    )
    def test_benchmark(self, benchmark, benchmark_data):
        benchmark(instrumental_broaden, *benchmark_data, 400)


class TestRotationalBroaden:
    @pytest.mark.parametrize("vsini", [-20, -1.00, -np.finfo(np.float64).eps, 0])
    def test_bad_fwhm(self, mock_data, vsini):
        with pytest.raises(ValueError):
            rotational_broaden(*mock_data, vsini)

    def test_rot_broadening_inst(self, mock_data):
        flux = rotational_broaden(*mock_data, 84)
        assert not np.allclose(flux, mock_data[1])

    def test_many_fluxes(self, mock_data):
        flux_stack = np.tile(mock_data[1], (4, 1))
        fluxes = rotational_broaden(mock_data[0], flux_stack, 400)
        assert fluxes.shape == flux_stack.shape
        assert not np.allclose(fluxes, flux_stack)

    @pytest.mark.parametrize(
        "benchmark_data", [100, 500, 1000, 5000, 10000], indirect=True
    )
    def test_benchmark(self, benchmark, benchmark_data):
        benchmark(rotational_broaden, *benchmark_data, 84)


class TestResample:
    @pytest.mark.parametrize("wave", [np.linspace(-1, -0.5), np.linspace(0, 1e4)])
    def test_bad_waves(self, mock_data, wave):
        with pytest.raises(ValueError):
            resample(*mock_data, wave)

    def test_resample(self, mock_data):
        dv = calculate_dv(mock_data[0])
        new_wave = create_log_lam_grid(dv, mock_data[0].min(), mock_data[0].max())["wl"]
        flux = resample(*mock_data, new_wave)
        assert flux.shape == new_wave.shape

    def test_many_fluxes(self, mock_data):
        dv = calculate_dv(mock_data[0])
        new_wave = create_log_lam_grid(dv, mock_data[0].min(), mock_data[0].max())["wl"]
        flux_stack = np.tile(mock_data[1], (4, 1))
        fluxes = resample(mock_data[0], flux_stack, new_wave)
        assert fluxes.shape == (4, len(new_wave))

    @pytest.mark.parametrize(
        "benchmark_data", [100, 500, 1000, 5000, 10000], indirect=True
    )
    def test_benchmark(self, benchmark, benchmark_data):
        wave, flux = benchmark_data
        dv = calculate_dv(wave)
        new_wave = create_log_lam_grid(dv, wave.min(), wave.max())["wl"]
        benchmark(resample, wave, flux, new_wave)


class TestDopplerShift:
    def test_no_change(self, mock_data):
        wave = doppler_shift(mock_data[0], 0)
        assert np.allclose(wave, mock_data[0])

    def test_blueshift(self, mock_data):
        wave = doppler_shift(mock_data[0], -1e3)
        assert np.all(wave < mock_data[0])

    def test_redshit(self, mock_data):
        wave = doppler_shift(mock_data[0], 1e3)
        assert np.all(wave > mock_data[0])

    def test_regression(self, mock_data):
        wave = doppler_shift(doppler_shift(mock_data[0], 1e3), -1e3)
        assert np.allclose(wave, mock_data[0])

    @pytest.mark.parametrize(
        "benchmark_data", [100, 500, 1000, 5000, 10000], indirect=True
    )
    def test_benchmark(self, benchmark, benchmark_data):
        benchmark(doppler_shift, benchmark_data[0], 1e3)


class TestChebyshevCorrection:
    @pytest.mark.parametrize(
        "coeffs", [[1, 0.005, 0.003, 0], [1, -0.005, 0.0, -0.9], [1, 0, 0.88, 1.2]]
    )
    def test_transforms(self, mock_data, coeffs):
        flux = chebyshev_correct(*mock_data, coeffs)
        assert not np.allclose(flux, mock_data[1])

    def test_no_change(self, mock_data):
        flux = chebyshev_correct(*mock_data, [1, 0, 0, 0])
        assert np.allclose(flux, mock_data[1])

    def test_single_fix_c0(self, mock_data):
        with pytest.raises(ValueError):
            chebyshev_correct(*mock_data, [0.9, 0, 0, 0])

    @pytest.mark.parametrize(
        "benchmark_data", [100, 500, 1000, 5000, 10000], indirect=True
    )
    def test_benchmark(self, benchmark, benchmark_data):
        benchmark(chebyshev_correct, *benchmark_data, [1, 0, 0, 0])


class TestExtinct:
    laws = ["ccm89", "odonnell94", "calzetti00", "fitzpatrick99", "fm07"]
    Avs = [0.4, 0.6, 1, 1.2]
    Rvs = [2, 3.2, 4, 5]

    @pytest.mark.parametrize("law, Av, Rv", itertools.product(laws, Avs, Rvs))
    def test_extinct(self, mock_data, law, Av, Rv):
        flux = extinct(*mock_data, Av=Av, Rv=Rv, law=law)
        assert not np.allclose(flux, mock_data[1])

    @pytest.mark.parametrize("law", laws)
    def test_no_extinct(self, mock_data, law):
        flux = extinct(*mock_data, 0, 3.1, law)
        assert np.allclose(flux, mock_data[1])

    def test_bad_laws(self, mock_data):
        with pytest.raises(ValueError):
            extinct(*mock_data, 1.0, 2.2, law="hello")

    @pytest.mark.parametrize("Av,Rv", [(0.2, -1), (0.3, -np.finfo(np.float64).tiny)])
    def test_bad_av_rv(self, mock_data, Av, Rv):
        with pytest.raises(ValueError):
            extinct(*mock_data, law="ccm89", Av=Av, Rv=Rv)

    def test_many_fluxes(self, mock_data):
        flux_stack = np.tile(mock_data[1], (4, 1))
        fluxes = extinct(mock_data[0], flux_stack, 0.3)
        assert fluxes.shape == flux_stack.shape
        assert not np.allclose(fluxes, flux_stack)

    @pytest.mark.parametrize(
        "benchmark_data", [100, 500, 1000, 5000, 10000], indirect=True
    )
    def test_benchmark(self, benchmark, benchmark_data):
        benchmark(extinct, *benchmark_data, Av=0.3)


class TestRescale:
    @pytest.mark.parametrize("log_scale", [1, 2, 3, -124, -42.2, 0.5])
    def test_transform(self, mock_data, log_scale):
        scale = np.exp(log_scale)
        flux = rescale(mock_data[1], scale)
        assert np.allclose(flux, mock_data[1] * scale)

    def test_no_scale(self, mock_data):
        flux = rescale(mock_data[1], 1)
        assert np.allclose(flux, mock_data[1])

    def test_regression(self, mock_data):
        flux = rescale(rescale(mock_data[1], 0.01), 100)
        assert np.allclose(flux, mock_data[1])

    def test_many_fluxes(self, mock_data):
        flux_stack = np.tile(mock_data[1], (4, 1))
        fluxes = rescale(flux_stack, 2)
        assert fluxes.shape == flux_stack.shape
        assert not np.allclose(fluxes, flux_stack)

    @pytest.mark.parametrize(
        "benchmark_data", [100, 500, 1000, 5000, 10000], indirect=True
    )
    def test_benchmark(self, benchmark, benchmark_data):
        benchmark(rescale, benchmark_data[1], 10)


class TestRenorm:
    @pytest.fixture
    def mock_data2(self, mock_data):
        wave, flux = mock_data
        flux = rescale(flux, 70)
        yield wave, flux

    def test_transform(self, mock_data, mock_data2):
        flux = renorm(*mock_data, mock_data2[1])
        assert flux.shape == mock_data[1].shape
        assert np.allclose(flux, mock_data[1] * 70)
        assert np.allclose(flux, mock_data2[1])

    def test_no_scale(self, mock_data):
        flux = renorm(*mock_data, mock_data[1])
        assert np.allclose(flux, mock_data[1])

    def test_regression(self, mock_data, mock_data2):
        flux = renorm(*mock_data, mock_data2[1])
        flux = renorm(mock_data[0], flux, mock_data[1])
        assert np.allclose(flux, mock_data[1])

    def test_many_fluxes(self, mock_data, mock_data2):
        flux_stack = np.tile(mock_data[1], (4, 1))
        fluxes = renorm(mock_data[0], flux_stack, mock_data2[1])
        assert fluxes.shape == flux_stack.shape
        assert np.allclose(fluxes, flux_stack * 70)

    @pytest.mark.parametrize(
        "benchmark_data", [100, 500, 1000, 5000, 10000], indirect=True
    )
    def test_benchmark(self, benchmark, benchmark_data):
        benchmark(renorm, *benchmark_data, benchmark_data[1] * 1002)
