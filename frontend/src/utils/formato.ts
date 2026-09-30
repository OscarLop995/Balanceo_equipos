const formateadorPuntuacion = new Intl.NumberFormat("es", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

export function formatearPuntuacion(valor: number): string {
  return formateadorPuntuacion.format(valor);
}
