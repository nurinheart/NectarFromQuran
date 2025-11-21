"""
Quranic Verses Data - Thematic Collection
100 verses across 10 themes with Ibn Kathir tafsir excerpts
"""

# Thematic verses collection (10 themes × 10 verses = 100 verses)
THEMATIC_VERSES = {
    "Mercy": [
        {
            "surah": 39,
            "ayah": 53,
            "theme": "Mercy",
            "tafsir_excerpt": "This verse shows Allah's infinite mercy. No matter how great the sins, Allah's mercy is greater. The door of repentance is always open until the soul reaches the throat at death. This is why the believers always have hope and never despair of Allah's mercy."
        },
        {
            "surah": 7,
            "ayah": 156,
            "theme": "Mercy",
            "tafsir_excerpt": "Allah's mercy encompasses all things. His mercy is vast and includes all of creation. Those who are conscious of Allah and follow His guidance will receive special mercy in this life and the hereafter."
        },
        {
            "surah": 21,
            "ayah": 107,
            "theme": "Mercy",
            "tafsir_excerpt": "The Prophet Muhammad ﷺ was sent as a mercy to all worlds - not just Muslims, but all of humanity, jinn, and even animals. His teachings bring mercy, justice, and guidance to those who follow them."
        },
        {
            "surah": 6,
            "ayah": 54,
            "theme": "Mercy",
            "tafsir_excerpt": "Allah has prescribed mercy upon Himself. When a servant sins then repents sincerely, Allah forgives. This shows us that mercy is an attribute Allah has made obligatory upon Himself out of His infinite wisdom."
        },
        {
            "surah": 11,
            "ayah": 90,
            "theme": "Mercy",
            "tafsir_excerpt": "Seeking forgiveness and turning back to Allah brings His mercy. Allah is Most Forgiving and Most Merciful to those who repent. His love for those who turn to Him is greater than a mother's love for her child."
        },
        {
            "surah": 2,
            "ayah": 218,
            "theme": "Mercy",
            "tafsir_excerpt": "Those who believe, migrate for Allah's sake, and strive in His path can expect Allah's mercy. These acts of sacrifice and devotion are met with divine mercy and reward both in this life and the next."
        },
        {
            "surah": 33,
            "ayah": 43,
            "theme": "Mercy",
            "tafsir_excerpt": "Allah and His angels send blessings upon the believers. This is a manifestation of divine mercy - that Allah mentions His servants and praises them, and the angels pray for their forgiveness and guidance."
        },
        {
            "surah": 17,
            "ayah": 82,
            "theme": "Mercy",
            "tafsir_excerpt": "The Quran itself is a mercy and healing for believers. It heals spiritual diseases, removes doubts, and brings peace to the heart. Reading it with reflection brings divine mercy into one's life."
        },
        {
            "surah": 30,
            "ayah": 21,
            "theme": "Mercy",
            "tafsir_excerpt": "Marriage and the love between spouses is a sign of Allah's mercy. The tranquility, love, and compassion in marriage relationships reflect divine mercy and are means of attaining His pleasure."
        },
        {
            "surah": 16,
            "ayah": 64,
            "theme": "Mercy",
            "tafsir_excerpt": "The Quran was revealed as guidance, mercy, and good news for Muslims. It clarifies matters people differ about and guides to the straight path. This is one of Allah's greatest mercies to humanity."
        }
    ],
    
    "Patience": [
        {
            "surah": 2,
            "ayah": 153,
            "theme": "Patience",
            "tafsir_excerpt": "Seeking help through patience and prayer is the way of the believers. When facing difficulties, turning to Allah through patient perseverance and establishing prayer brings divine support and relief."
        },
        {
            "surah": 2,
            "ayah": 155,
            "theme": "Patience",
            "tafsir_excerpt": "Allah tests believers with fear, hunger, loss of wealth, lives, and fruits as a means of purification and elevation of ranks. Those who remain patient during these trials earn great rewards."
        },
        {
            "surah": 39,
            "ayah": 10,
            "theme": "Patience",
            "tafsir_excerpt": "The patient will receive their reward without account. This means their reward is so vast it cannot be calculated. Patience in obedience, patience in avoiding sin, and patience during calamities all bring immense rewards."
        },
        {
            "surah": 3,
            "ayah": 200,
            "theme": "Patience",
            "tafsir_excerpt": "Believers are commanded to be patient, compete in patience with others, and maintain their positions of faith. Being conscious of Allah while exercising patience leads to ultimate success."
        },
        {
            "surah": 16,
            "ayah": 126,
            "theme": "Patience",
            "tafsir_excerpt": "Patience is better than revenge. While it is permissible to retaliate justly, exercising patience and forgiveness is nobler and brings greater reward from Allah."
        },
        {
            "surah": 103,
            "ayah": 3,
            "theme": "Patience",
            "tafsir_excerpt": "Success requires faith, good deeds, and mutually enjoining truth and patience. Encouraging each other to be patient strengthens the community and helps everyone maintain steadfastness on the right path."
        },
        {
            "surah": 11,
            "ayah": 115,
            "theme": "Patience",
            "tafsir_excerpt": "Be patient, for Allah does not waste the reward of the good-doers. Every moment of patience is recorded and will be rewarded. Allah sees all struggles and will compensate them fully."
        },
        {
            "surah": 40,
            "ayah": 55,
            "theme": "Patience",
            "tafsir_excerpt": "The Prophet ﷺ was commanded to be patient and seek forgiveness. If even the best of creation needed patience, how much more do we need it? Combining patience with seeking forgiveness is a powerful formula."
        },
        {
            "surah": 46,
            "ayah": 35,
            "theme": "Patience",
            "tafsir_excerpt": "Be patient as were the messengers of firm resolve. Looking at the patience of previous prophets in the face of persecution and hardship inspires us to be patient with our much smaller trials."
        },
        {
            "surah": 70,
            "ayah": 5,
            "theme": "Patience",
            "tafsir_excerpt": "Be patient with beautiful patience - patience without complaint or despair. This is the highest form of patience where one accepts Allah's decree with contentment while trusting His perfect wisdom."
        }
    ],
    
    "Gratitude": [
        {
            "surah": 14,
            "ayah": 7,
            "theme": "Gratitude",
            "tafsir_excerpt": "If you are grateful, Allah will increase you in blessings. This is a divine promise - gratitude leads to more blessings. Conversely, ingratitude leads to punishment. Count your blessings and thank Allah constantly."
        },
        {
            "surah": 2,
            "ayah": 152,
            "theme": "Gratitude",
            "tafsir_excerpt": "Remember Allah and He will remember you. Be grateful and do not be ungrateful. Divine remembrance is the foundation of gratitude, and ingratitude is a serious sin that blocks blessings."
        },
        {
            "surah": 16,
            "ayah": 18,
            "theme": "Gratitude",
            "tafsir_excerpt": "If you try to count Allah's blessings, you cannot enumerate them. The blessings are countless - health, family, sustenance, guidance. Recognizing our inability to count them should increase our gratitude."
        },
        {
            "surah": 27,
            "ayah": 40,
            "theme": "Gratitude",
            "tafsir_excerpt": "Gratitude benefits the grateful person themselves. When we thank Allah, we're not benefiting Him but ourselves. Allah is Self-Sufficient and doesn't need our gratitude, but we need to be grateful."
        },
        {
            "surah": 31,
            "ayah": 12,
            "theme": "Gratitude",
            "tafsir_excerpt": "Luqman was given wisdom, and the essence of wisdom is gratitude to Allah. A truly wise person recognizes all blessings come from Allah and expresses gratitude through words and actions."
        },
        {
            "surah": 39,
            "ayah": 66,
            "theme": "Gratitude",
            "tafsir_excerpt": "Worship Allah alone and be among the grateful. True worship includes gratitude. Gratitude is shown through submission to Allah, using His blessings in His obedience, and thanking Him constantly."
        },
        {
            "surah": 76,
            "ayah": 3,
            "theme": "Gratitude",
            "tafsir_excerpt": "Allah guided humanity to the right path, whether we're grateful or ungrateful. The choice is ours - will we recognize this blessing of guidance and be grateful, or will we deny it?"
        },
        {
            "surah": 3,
            "ayah": 123,
            "theme": "Gratitude",
            "tafsir_excerpt": "Allah helped you at Badr when you were few and weak. Be conscious of Allah so you may be grateful. Remembering past victories and blessings should motivate us to be grateful and maintain our faith."
        },
        {
            "surah": 56,
            "ayah": 70,
            "theme": "Gratitude",
            "tafsir_excerpt": "Fresh water is one of Allah's greatest blessings. Do you thank Allah for it? We often take basic blessings like water for granted, yet they sustain our very existence."
        },
        {
            "surah": 16,
            "ayah": 78,
            "theme": "Gratitude",
            "tafsir_excerpt": "Allah brought you out of your mothers' wombs knowing nothing, and gave you hearing, sight, and hearts - that you may be grateful. Every faculty we have is a blessing deserving gratitude."
        }
    ],
    
    "Prayer": [
        {
            "surah": 2,
            "ayah": 45,
            "theme": "Prayer",
            "tafsir_excerpt": "Seek help through patience and prayer. It is difficult except for the humble. Prayer is heavy for those who don't have humility before Allah, but for the humble believers, it is comfort and joy."
        },
        {
            "surah": 20,
            "ayah": 14,
            "theme": "Prayer",
            "tafsir_excerpt": "Allah declares His oneness and commands establishment of prayer for His remembrance. Prayer is the best form of remembering Allah, involving physical, verbal, and spiritual acts of worship."
        },
        {
            "surah": 29,
            "ayah": 45,
            "theme": "Prayer",
            "tafsir_excerpt": "Prayer prevents immorality and wrongdoing. Remembrance of Allah is greatest. Properly performed prayer with focus creates a shield against sins and keeps one connected to Allah."
        },
        {
            "surah": 11,
            "ayah": 114,
            "theme": "Prayer",
            "tafsir_excerpt": "Establish prayer at both ends of the day and in some hours of the night. Good deeds remove misdeeds. This shows prayer, especially at designated times, expiates sins and purifies the soul."
        },
        {
            "surah": 17,
            "ayah": 78,
            "theme": "Prayer",
            "tafsir_excerpt": "Establish prayer from the decline of the sun until the darkness of night, and recite the Quran at dawn. The Fajr prayer is particularly virtuous and witnessed by angels changing shifts."
        },
        {
            "surah": 2,
            "ayah": 238,
            "theme": "Prayer",
            "tafsir_excerpt": "Maintain all prayers especially the middle prayer, and stand before Allah devoutly obedient. Consistency in prayer and maintaining proper devotion is crucial for spiritual success."
        },
        {
            "surah": 70,
            "ayah": 23,
            "theme": "Prayer",
            "tafsir_excerpt": "Those who are constant in their prayers - consistency is key. Not just praying occasionally but maintaining regular prayer throughout life is a characteristic of successful believers."
        },
        {
            "surah": 107,
            "ayah": 5,
            "theme": "Prayer",
            "tafsir_excerpt": "Woe to those who are heedless of their prayers - praying with delay, negligence, or showing off. Prayer must be performed on time, with focus, and sincerely for Allah alone."
        },
        {
            "surah": 4,
            "ayah": 103,
            "theme": "Prayer",
            "tafsir_excerpt": "When you complete the prayer, remember Allah standing, sitting, and lying down. Prayer is not just the formal ritual - it should lead to constant remembrance of Allah in all states."
        },
        {
            "surah": 50,
            "ayah": 40,
            "theme": "Prayer",
            "tafsir_excerpt": "Glorify Allah in the night and after prostrations. Night worship and extra prayers beyond obligatory ones bring one closer to Allah and erase sins."
        }
    ],
    
    "Family": [
        {
            "surah": 17,
            "ayah": 23,
            "theme": "Family",
            "tafsir_excerpt": "Your Lord has decreed that you worship none but Him, and be kind to parents. Whether one or both reach old age, do not say 'uff' to them or repel them, but speak honorably. Parents' rights are immediately after Allah's rights."
        },
        {
            "surah": 31,
            "ayah": 14,
            "theme": "Family",
            "tafsir_excerpt": "We enjoined upon man to be good to his parents. His mother carried him in weakness upon weakness. The physical and emotional sacrifice of mothers especially deserves recognition and gratitude."
        },
        {
            "surah": 4,
            "ayah": 1,
            "theme": "Family",
            "tafsir_excerpt": "Be conscious of Allah and maintain family ties. Allah is ever watchful over you. Maintaining kinship ties is obligatory and cutting them is a major sin that prevents entry to Paradise."
        },
        {
            "surah": 30,
            "ayah": 21,
            "theme": "Family",
            "tafsir_excerpt": "Among His signs is that He created for you spouses that you may find tranquility in them, and He placed between you affection and mercy. Marriage is a sign of Allah's power and mercy."
        },
        {
            "surah": 66,
            "ayah": 6,
            "theme": "Family",
            "tafsir_excerpt": "Believers, protect yourselves and your families from a Fire. Each person is responsible not just for themselves but for guiding and protecting their family from Hell through proper Islamic upbringing."
        },
        {
            "surah": 25,
            "ayah": 74,
            "theme": "Family",
            "tafsir_excerpt": "Grant us from our spouses and children comfort to our eyes and make us leaders for the righteous. A righteous family that worships Allah together is one of the greatest blessings."
        },
        {
            "surah": 13,
            "ayah": 21,
            "theme": "Family",
            "tafsir_excerpt": "Those who join what Allah has ordered to be joined - maintaining family ties - and fear their Lord. Keeping family connections strong is part of fearing Allah and will be rewarded."
        },
        {
            "surah": 24,
            "ayah": 32,
            "theme": "Family",
            "tafsir_excerpt": "Marry the unmarried among you. If they are poor, Allah will enrich them from His bounty. Marriage is encouraged and Allah promises to provide for those who marry seeking His pleasure."
        },
        {
            "surah": 2,
            "ayah": 233,
            "theme": "Family",
            "tafsir_excerpt": "Mothers may breastfeed their children for two complete years. The father must provide for them and clothe them reasonably. Family responsibilities are clearly defined with rights and duties for all."
        },
        {
            "surah": 46,
            "ayah": 15,
            "theme": "Family",
            "tafsir_excerpt": "We have enjoined upon man goodness to parents. Show me how to be grateful for Your favor upon me and my parents. Recognizing parents as a blessing from Allah increases our gratitude and kindness toward them."
        }
    ],
    
    "Knowledge": [
        {
            "surah": 20,
            "ayah": 114,
            "theme": "Knowledge",
            "tafsir_excerpt": "Say: My Lord, increase me in knowledge. The Prophet ﷺ was commanded to ask for more knowledge, showing its immense importance. Knowledge of Islam brings one closer to Allah."
        },
        {
            "surah": 96,
            "ayah": 1,
            "theme": "Knowledge",
            "tafsir_excerpt": "Read in the name of your Lord who created. The first revelation emphasizes reading and learning. Islam highly values knowledge and literacy as means of understanding creation and the Creator."
        },
        {
            "surah": 39,
            "ayah": 9,
            "theme": "Knowledge",
            "tafsir_excerpt": "Are those who know equal to those who do not know? People of understanding will remember. Knowledge elevates one's status before Allah and enables proper understanding and application of religion."
        },
        {
            "surah": 58,
            "ayah": 11,
            "theme": "Knowledge",
            "tafsir_excerpt": "Allah will raise those who believe among you and those given knowledge by degrees. Both faith and knowledge lead to elevated ranks with Allah in this life and the next."
        },
        {
            "surah": 35,
            "ayah": 28,
            "theme": "Knowledge",
            "tafsir_excerpt": "Only those of Allah's servants who have knowledge truly fear Him. The more one knows about Allah - His names, attributes, and signs in creation - the more one fears and loves Him."
        },
        {
            "surah": 16,
            "ayah": 43,
            "theme": "Knowledge",
            "tafsir_excerpt": "Ask the people of knowledge if you do not know. When we lack knowledge about religious matters, we must ask qualified scholars rather than following ignorance."
        },
        {
            "surah": 17,
            "ayah": 36,
            "theme": "Knowledge",
            "tafsir_excerpt": "Do not pursue what you have no knowledge of. Hearing, sight, and hearts will all be questioned. We're accountable for how we use these faculties - we must seek certain knowledge."
        },
        {
            "surah": 4,
            "ayah": 113,
            "theme": "Knowledge",
            "tafsir_excerpt": "Allah has revealed to you the Book and wisdom and taught you what you did not know. The Quran and Sunnah are the greatest sources of knowledge, teaching us what benefits us in both worlds."
        },
        {
            "surah": 2,
            "ayah": 269,
            "theme": "Knowledge",
            "tafsir_excerpt": "Whoever is given wisdom has been given much good. Wisdom is understanding and applying knowledge correctly. It's one of the greatest gifts Allah grants to His servants."
        },
        {
            "surah": 55,
            "ayah": 4,
            "theme": "Knowledge",
            "tafsir_excerpt": "He taught man eloquence. The ability to express knowledge clearly through speech is a blessing from Allah, enabling us to convey truth and benefit others."
        }
    ],
    
    "Trust_in_Allah": [
        {
            "surah": 65,
            "ayah": 3,
            "theme": "Trust in Allah",
            "tafsir_excerpt": "Whoever relies upon Allah, then He is sufficient for him. Allah accomplishes His purpose. When we truly trust Allah, He takes care of all our affairs and provides from unexpected sources."
        },
        {
            "surah": 3,
            "ayah": 159,
            "theme": "Trust in Allah",
            "tafsir_excerpt": "When you have made a decision, put your trust in Allah. After consulting and deciding, rely completely on Allah. He loves those who trust in Him and rely on Him for success."
        },
        {
            "surah": 8,
            "ayah": 49,
            "theme": "Trust in Allah",
            "tafsir_excerpt": "Whoever relies upon Allah - indeed, Allah is Mighty and Wise. Trusting Allah means knowing He is capable of all things and His decisions are based on perfect wisdom."
        },
        {
            "surah": 9,
            "ayah": 51,
            "theme": "Trust in Allah",
            "tafsir_excerpt": "Nothing will happen to us except what Allah has decreed for us. Let the believers put their trust in Allah. True trust means accepting Allah's decree with contentment."
        },
        {
            "surah": 11,
            "ayah": 123,
            "theme": "Trust in Allah",
            "tafsir_excerpt": "To Allah belongs the unseen of the heavens and earth, and to Him all matters are returned. So worship Him and put your trust in Him. Only Allah knows and controls everything."
        },
        {
            "surah": 12,
            "ayah": 67,
            "theme": "Trust in Allah",
            "tafsir_excerpt": "The decision rests only with Allah. In Him I trust, and in Him let those who trust put their trust. Prophet Jacob showed perfect trust even when facing the loss of his sons."
        },
        {
            "surah": 14,
            "ayah": 11,
            "theme": "Trust in Allah",
            "tafsir_excerpt": "Upon Allah let the believers rely. When facing opposition for speaking truth, prophets trusted Allah completely. We should follow their example in relying on Allah alone."
        },
        {
            "surah": 25,
            "ayah": 58,
            "theme": "Trust in Allah",
            "tafsir_excerpt": "Rely upon the Ever-Living who does not die. He is the only One who never fails or dies, making Him the only one truly worthy of complete trust and reliance."
        },
        {
            "surah": 33,
            "ayah": 3,
            "theme": "Trust in Allah",
            "tafsir_excerpt": "Put your trust in Allah, for Allah is sufficient as a Trustee. When we fulfill our responsibilities and trust Allah with the results, He takes care of everything."
        },
        {
            "surah": 39,
            "ayah": 38,
            "theme": "Trust in Allah",
            "tafsir_excerpt": "Upon Allah let those who trust rely. After acknowledging Allah as Creator and Provider, the natural conclusion is to trust Him completely with all our affairs."
        }
    ],
    
    "Charity": [
        {
            "surah": 2,
            "ayah": 261,
            "theme": "Charity",
            "tafsir_excerpt": "The example of those who spend in Allah's way is like a grain that grows seven ears, with a hundred grains in each ear. Allah multiplies for whom He wills. Charity is investment with Allah, returning multiplied rewards."
        },
        {
            "surah": 2,
            "ayah": 274,
            "theme": "Charity",
            "tafsir_excerpt": "Those who spend their wealth by night and day, secretly and publicly, will have their reward with their Lord. No fear for them, nor will they grieve. All forms of giving are rewarded."
        },
        {
            "surah": 57,
            "ayah": 18,
            "theme": "Charity",
            "tafsir_excerpt": "Those who give charity - it will be multiplied for them, and they will have a generous reward. What we give in charity doesn't decrease our wealth but increases it with Allah."
        },
        {
            "surah": 9,
            "ayah": 103,
            "theme": "Charity",
            "tafsir_excerpt": "Take from their wealth charity to purify and sanctify them. Charity purifies wealth and the soul, removing greed and attachment to material possessions."
        },
        {
            "surah": 64,
            "ayah": 16,
            "theme": "Charity",
            "tafsir_excerpt": "Be conscious of Allah as much as possible, and listen, obey, and spend - it is better for yourselves. Spending in charity benefits the giver more than the receiver."
        },
        {
            "surah": 2,
            "ayah": 267,
            "theme": "Charity",
            "tafsir_excerpt": "Give from the good things you have earned and what We have produced for you from the earth. Give quality charity, not the worst of what you have, as you wouldn't accept that yourself."
        },
        {
            "surah": 2,
            "ayah": 271,
            "theme": "Charity",
            "tafsir_excerpt": "If you give charity publicly, it is good, but if you conceal it and give to the poor, it is better and will expiate some of your sins. Secret charity is more sincere and removes show-off."
        },
        {
            "surah": 3,
            "ayah": 92,
            "theme": "Charity",
            "tafsir_excerpt": "You will never attain righteousness until you spend from what you love. True generosity means giving what you value, not just excess. This reflects genuine faith and love for Allah."
        },
        {
            "surah": 63,
            "ayah": 10,
            "theme": "Charity",
            "tafsir_excerpt": "Spend from what We have provided before death comes and you say: 'If only I had a little more time to give charity.' Give now, for tomorrow's chance is not guaranteed."
        },
        {
            "surah": 30,
            "ayah": 39,
            "theme": "Charity",
            "tafsir_excerpt": "What you give in charity, seeking Allah's pleasure - it is those whose reward will be multiplied. Intention matters - charity must be for Allah's sake to receive divine multiplication."
        }
    ],
    
    "Guidance": [
        {
            "surah": 1,
            "ayah": 6,
            "theme": "Guidance",
            "tafsir_excerpt": "Guide us to the straight path - the path we ask Allah for in every prayer. This is the path of those who earned Allah's favor, not of those who went astray. Constant guidance is needed to stay on the right path."
        },
        {
            "surah": 2,
            "ayah": 2,
            "theme": "Guidance",
            "tafsir_excerpt": "This is the Book about which there is no doubt, a guidance for the God-conscious. The Quran is the ultimate guide, but only those who are conscious of Allah benefit from its guidance."
        },
        {
            "surah": 17,
            "ayah": 9,
            "theme": "Guidance",
            "tafsir_excerpt": "This Quran guides to what is most suitable and gives good news to believers who do righteous deeds. The Quran provides the best guidance for all aspects of life."
        },
        {
            "surah": 6,
            "ayah": 90,
            "theme": "Guidance",
            "tafsir_excerpt": "Those are the ones Allah has guided, so follow their guidance. The prophets are our role models. Following their example is the key to being rightly guided."
        },
        {
            "surah": 16,
            "ayah": 36,
            "theme": "Guidance",
            "tafsir_excerpt": "We sent a messenger to every nation saying: Worship Allah and avoid false gods. Guidance through messengers is Allah's mercy to all people throughout history."
        },
        {
            "surah": 28,
            "ayah": 56,
            "theme": "Guidance",
            "tafsir_excerpt": "You cannot guide whom you love, but Allah guides whom He wills. Even prophets cannot force guidance - it comes from Allah to those who sincerely seek it."
        },
        {
            "surah": 42,
            "ayah": 52,
            "theme": "Guidance",
            "tafsir_excerpt": "We have made the Quran a light by which We guide whom We will of Our servants. And indeed, you guide to a straight path. The Quran illuminates the way forward."
        },
        {
            "surah": 5,
            "ayah": 16,
            "theme": "Guidance",
            "tafsir_excerpt": "Allah guides whoever seeks His pleasure to ways of peace and brings them out from darkness into light. Seeking Allah's pleasure is the key to receiving His guidance."
        },
        {
            "surah": 76,
            "ayah": 3,
            "theme": "Guidance",
            "tafsir_excerpt": "We showed him the way, whether he be grateful or ungrateful. Allah has made the path clear - the choice to follow it or reject it is ours."
        },
        {
            "surah": 7,
            "ayah": 43,
            "theme": "Guidance",
            "tafsir_excerpt": "We would never have been guided if Allah had not guided us. The messengers of our Lord came with truth. All guidance ultimately comes from Allah."
        }
    ],
    
    "Hope": [
        {
            "surah": 12,
            "ayah": 87,
            "theme": "Hope",
            "tafsir_excerpt": "Do not despair of Allah's mercy. Only disbelievers despair of Allah's mercy. No matter how difficult the situation, believers always maintain hope in Allah's relief."
        },
        {
            "surah": 94,
            "ayah": 5,
            "theme": "Hope",
            "tafsir_excerpt": "With hardship comes ease. Mentioned twice for emphasis - relief follows difficulty. This divine promise gives hope during trials that ease is coming."
        },
        {
            "surah": 2,
            "ayah": 214,
            "theme": "Hope",
            "tafsir_excerpt": "When will Allah's help come? Indeed, Allah's help is near. During trials, we may feel despair, but Allah's help is always near for those who remain patient."
        },
        {
            "surah": 11,
            "ayah": 9,
            "theme": "Hope",
            "tafsir_excerpt": "If We give man a taste of mercy then withdraw it, he becomes despairing. But believers maintain hope even when blessings are temporarily withdrawn, trusting Allah's wisdom."
        },
        {
            "surah": 40,
            "ayah": 60,
            "theme": "Hope",
            "tafsir_excerpt": "Your Lord says: Call upon Me; I will respond to you. This is a promise - Allah answers every sincere supplication, giving us hope that our prayers are heard."
        },
        {
            "surah": 3,
            "ayah": 139,
            "theme": "Hope",
            "tafsir_excerpt": "Do not lose hope, nor grieve, for you will be superior if you are true believers. Believers face setbacks with hope, knowing ultimate victory belongs to the faithful."
        },
        {
            "surah": 65,
            "ayah": 2,
            "theme": "Hope",
            "tafsir_excerpt": "Whoever is conscious of Allah, He will make a way out for him and provide from where he does not expect. This gives hope that Allah will solve problems in unexpected ways."
        },
        {
            "surah": 29,
            "ayah": 5,
            "theme": "Hope",
            "tafsir_excerpt": "Whoever hopes for the meeting with Allah - Allah's appointed time is coming. The ultimate hope is meeting Allah in Paradise. This hope motivates righteous action."
        },
        {
            "surah": 18,
            "ayah": 110,
            "theme": "Hope",
            "tafsir_excerpt": "Whoever hopes for the meeting with his Lord, let him do righteous work. Hope in Allah's reward must be accompanied by righteous deeds."
        },
        {
            "surah": 33,
            "ayah": 47,
            "theme": "Hope",
            "tafsir_excerpt": "Give believers good news that they will have great bounty from Allah. The Quran constantly gives believers reasons for optimism and hope through its promises."
        }
    ]
}


def get_all_verses():
    """Get all 100 verses from all themes"""
    all_verses = []
    for theme, verses in THEMATIC_VERSES.items():
        all_verses.extend(verses)
    return all_verses


def get_verses_by_theme(theme_name):
    """Get verses for a specific theme"""
    return THEMATIC_VERSES.get(theme_name, [])


def get_theme_count():
    """Get number of themes"""
    return len(THEMATIC_VERSES)


def get_total_verses():
    """Get total number of verses"""
    return sum(len(verses) for verses in THEMATIC_VERSES.values())
