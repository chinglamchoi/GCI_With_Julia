contin = true
winloss = [["draw", "win", "lose"], ["lose", "draw", "win"], ["win", "lose", "draw"]]
actions = ["rock", "paper", "scissors"]

while contin
	#let 1:rock, 2:paper, 3:scissors
	AI = rand(1:3)
	println("Please select 1 for rock, 2 for paper, 3 for scissors")
	human = parse(Int64, readline())
	println("AI played " * actions[AI])
	println("You " * winloss[AI][human] * "! Do you want to continue: true/false?")
	again = parse(Bool, readline())
	!again && break
end
