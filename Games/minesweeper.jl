println("Which grid do you want to try? 8 or 16?")
num = parse(Int64, readline())

global usergrid = Array{Array{String,1}, 1}(undef, num)
global ansgrid = Array{Array{Int64,1}, 1}(undef, num)
temp = fill("_", num)
tempa = fill(0, num)

for i in 1:num
	usergrid[i] = deepcopy(temp)
	ansgrid[i] = deepcopy(tempa)
end


num == 8 ? mines = 9 : mines= 20
mgrid = Array{Array{Int64, 1}}(undef, mines)
distinct = Set()

for i in 1:mines
	z = length(distinct)
	while true
		try_ = [rand(1:num), rand(1:num)]
		push!(distinct, try_)
		t = length(distinct) != z
		t && (mgrid[i] = try_)
		t && break
	end
end
#tester: mgrid = [[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[1,8],[2,1]]


for i in 1:mines 
	x,y = mgrid[i][1], mgrid[i][2]
	global ansgrid[x][y] = 9
	change = [[x-1, y-1], [x-1, y], [x-1, y+1], [x, y-1], [x, y+1], [x+1, y-1], [x+1, y], [x+1, y+1]]
	for j in 1:8
		try
			global ansgrid[change[j][1]][change[j][2]] += 1
		catch e
			cc = 1
		end
	end
end


function g(x,y,z, w)
	global usergrid, ansgrid, mgrid
	if z
		for i in 1:mines 
			global usergrid[mgrid[i][1]][mgrid[i][2]] = "X"
		end
		!w && println("Game over! Here is the board:")
	else
		global usergrid[x][y] = string(ansgrid[x][y])
	end
	display(usergrid)
end
		


f(x,y) = ansgrid[x][y] >= 9 ? true : false #

global ch = Set()
while true
	wincon = ((length(ch) == (64 - mines)) && (num==8)) || ((length(ch) == (256 - mines)) && (num==16))
	wincon && println("You win!! Here is the board:\n")
	wincon && g(1,1,true, wincon)
	wincon && break
	print("Which cell do you want to reveal? Enter in format \"column row\": ")
	c, r = split(readline(), " ")
	c,r = parse(Int64, c), parse(Int64, r)
	push!(ch, [c, r])
	valid = f(c,r)
	g(c,r,valid, wincon)
	println("\n")
	valid && break
end
