function y = f(x)
  y = exp(1/x)/(x^2);
endfunction;
[q, ier, nfun, err] = quad(@f, 1, 2);
q