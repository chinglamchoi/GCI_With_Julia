import Base: ==, -
logs = ["rock", "paper", "scissors"]

abstract type Action end
struct Rock <: Action name::Int64 end
struct Paper <: Action name::Int64 end
struct Scissors <: Action name::Int64 end

AI = rand(1:3)
println("Please choose 1 for rock, 2 for paper, 3 for scissors: ")
human = parse(Int64, readline())

type(x) = x == 2 ? Paper(2) : (x < 2 ? Rock(1) : Scissors(3))
AI_choice = type(AI)
Human_choice = type(human)
println("AI chose " * logs[AI])

==(x::Action, y::Action) = typeof(x) == typeof(y) ? true : false
-(x::Action, y::Action) = x.name - y.name

(AI_choice == Human_choice) ? println("You draw!") : (((Human_choice - AI_choice == 1) || (Human_choice - AI_choice == -2)) ? println("You win!") : println("You lose!"))