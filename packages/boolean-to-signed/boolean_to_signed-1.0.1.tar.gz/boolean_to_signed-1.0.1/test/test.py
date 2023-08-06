from boolean_to_signed import to_signed

print(to_signed(False));                  #=> -1
print(to_signed(True));                   #=> 1


# use cases
x = y = value = 0

#  using naive conditional assignment
if x > 0:
  y += value
else:
  y -= value;

# using direct assignment
y += to_signed(x > 0) * value;

print(y)