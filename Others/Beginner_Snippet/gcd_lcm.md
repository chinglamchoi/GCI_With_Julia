---
title: GCD and LCM
tags: math,advanced
---

Computes the Greatest Common Denominator (GCD) and Least Common Mutiple (LCM) of 2 numbers a,b.

This implementation uses knowledge of the Euclidean Algorithm to achieve better time complexity & simpler code. 
Euclidean Algorithm: For all a,b s.t. a > b, there exists some q,r for which a=q*b+r is true, with r < b or r = 0

```jl
function gcd(a,b)
    if b == 0
        return a
    end
    return gcd(b, a%b)
end
```

```jl
function lcm(a,b)
    return Int64((a*b)/gcd(a,b))
end
```

```jl
a,b = split(readline(), " ")
a,b = parse(Int64, a), parse(Int64, b)
result = gcd(a,b)
result1 = lcm(a,b)
println("The GCD of ", a, " and ", b, " is ", result, ".")
println("The LCM of ", a, " and ", b, " is ", result1, ".")
```
