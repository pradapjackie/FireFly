export const convertHexToRGB = (hex) => {
  if (hex.match('rgba')) {
    return hex.slice(5).split(',').slice(0, -1).join(',');
  }

  if (/^#([A-Fa-f\d]{3}){1,2}$/.test(hex)) {
    let c;
    c = hex.substring(1).split('');
    if (c.length === 3) {
      c = [c[0], c[0], c[1], c[1], c[2], c[2]];
    }
    c = `0x${c.join('')}`;

    return [(c >> 16) & 255, (c >> 8) & 255, c & 255].join(',');
  }
};
